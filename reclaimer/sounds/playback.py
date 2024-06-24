#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import threading
import time
from traceback import format_exc

try:
    import simpleaudio
except ImportError:
    simpleaudio = None

from reclaimer.sounds import audioop, constants, util,\
    blam_sound_permutation, sound_decompilation as sound_decomp


def build_wave_object(sample_data, encoding, compression, sample_rate):
    #print("CREATING WAVE OBJECT")
    if not simpleaudio:
        raise NotImplementedError(
            "Could not detect simpleaudio. Cannot build WaveObject."
            )

    channel_count = constants.channel_counts.get(encoding, 'unknown')
    sample_width  = constants.sample_widths.get(compression, 'unknown')
    if channel_count not in (1, 2):
        raise ValueError(
            "Cannot build WaveObject from audio with %s channels" % channel_count
            )
    elif sample_width not in (1, 2, 3, 4):
        raise ValueError(
            "Cannot build WaveObject from samples of %s byte width" % sample_width
            )

    if sample_width > 1 and util.is_big_endian_pcm(compression):
        sample_data = audioop.byteswap(sample_data, sample_width)

    return simpleaudio.WaveObject(
        sample_data, channel_count, sample_width, sample_rate
        )


def wave_object_from_blam_sound_perm(blam_perm):
    samples = getattr(blam_perm, "source_sample_data", None)
    comp    = getattr(blam_perm, "source_compression", None)
    enc     = getattr(blam_perm, "source_encoding",    None)
    sr      = getattr(blam_perm, "source_sample_rate", None)
    if blam_perm and (not samples or comp not in constants.PCM_FORMATS):
        comp = constants.COMPRESSION_PCM_16_LE
        if samples:
            # sample data is compressed in a format we can't 
            # linearly read, so we need to decompress it.
            samples = blam_perm.decompress_source_samples(comp, sr, enc)
        else:
            # if there is no source sample data, so we'll try 
            # to use the decompressed processed samples instead.
            blam_perm.regenerate_source(comp)
            samples = blam_perm.source_sample_data

    return build_wave_object(samples, enc, comp, sr) if samples else None


class SoundPlayerBase:
    _wave_objects = ()

    _play_objects_by_wave_ids = ()
    _player_locks_by_wave_ids = ()
    _force_stops_by_wave_ids = ()
    _merged_play_objects = ()
    _merged_player_lock = None
    _merged_force_stop = None

    pitch_range_index = -1
    permutation_index = -1
    separate_wave_queues   = True
    concatenate_perm_chain = True
    
    class ForceStop:
        _stop = False
        def __bool__(self): return self._stop
        def set(self, val): self._stop = bool(val)

    def __init__(self):
        self._wave_objects = {}
        self._play_objects_by_wave_ids = {}
        self._player_locks_by_wave_ids = {}
        self._force_stops_by_wave_ids = {}
        self._merged_play_objects = {}
        self._merged_player_lock = threading.Lock()
        self._merged_force_stop = SoundPlayerBase.ForceStop()

    def get_compression(self, wave_id=None):
        raise NotImplementedError("Must override this method")
    def get_sample_rate(self, wave_id=None):
        raise NotImplementedError("Must override this method")
    def get_encoding(self, wave_id=None):
        raise NotImplementedError("Must override this method")

    def get_play_objects(self, wave_id=None):
        wave_id = wave_id or self.get_wave_id()
        return (
            self._play_objects_by_wave_ids.setdefault(wave_id, {})
            if self.separate_wave_queues else
            self._merged_play_objects
            )

    def get_player_lock(self, wave_id=None):
        wave_id = wave_id or self.get_wave_id()
        return (
            self._player_locks_by_wave_ids.setdefault(wave_id, threading.Lock())
            if self.separate_wave_queues else
            self._merged_player_lock
            )

    def get_force_stop(self, wave_id=None):
        wave_id = wave_id or self.get_wave_id()
        return (
            self._force_stops_by_wave_ids.setdefault(wave_id, SoundPlayerBase.ForceStop())
            if self.separate_wave_queues else
            self._merged_force_stop
            )

    @property
    def pitch_ranges(self):
        raise NotImplementedError("Must override this method")
    @property
    def permutations(self):
        raise NotImplementedError("Must override this method")

    def get_wave_id(self, pr_index=None, perm_index=None):
        if pr_index is None:
            pr_index = self.pitch_range_index
        if perm_index is None:
            perm_index = self.permutation_index

        wave_id = (
            None if pr_index   not in self.pitch_ranges else pr_index, 
            None if perm_index not in self.permutations else perm_index, 
            )
        return None if None in wave_id else wave_id

    def get_pitch_range(self, pr_index=None):
        if pr_index is None:
            pr_index = self.pitch_range_index

        return self.pitch_ranges.get(pr_index)

    def get_permutation(self, pr_index=None, perm_index=None):
        if perm_index is None:
            perm_index = self.permutation_index

        pr = self.get_pitch_range(pr_index)
        return None if pr is None else pr.permutations.get(pr_index)

    def play_sound(self, wave_id=None, threaded=True):
        try:
            comp = self.get_compression(wave_id)
            if not (
                    (comp == constants.COMPRESSION_OGG  and constants.OGGVORBIS_AVAILABLE) or
                    (comp == constants.COMPRESSION_OPUS and constants.OPUS_AVAILABLE) or
                    (comp == constants.COMPRESSION_FLAC and constants.FLAC_AVAILABLE) or
                    (comp == constants.COMPRESSION_XBOX_ADPCM) or
                    (comp in constants.PCM_FORMATS)
                    ):
                print("Cannot play audio (unknown/unsupported compression: %s)." % comp)
                return

            wave_id = wave_id or self.get_wave_id()
            pr_index, perm_index = wave_id
            if None in wave_id:
                return

            wave_object = self._wave_objects.get(wave_id)

            # create the wave object if it doesnt exist yet
            if wave_object is None:
                blam_perm = self.get_permutation(pr_index, perm_index)
                if blam_perm is None:
                    return

                if not isinstance(blam_perm, blam_sound_permutation.BlamSoundPermutation):
                    perms = self.permutations
                    if self.concatenate_perm_chain:
                        permlist, _ = sound_decomp.get_tag_perm_chain(perms, perm_index)
                    elif perm_index in range(len(perms)):
                        permlist = [perms[perm_index]]
                    else:
                        permlist = []

                    blam_perm = sound_decomp.tag_perm_chain_to_blam_perm(
                        permlist, self.get_sample_rate(wave_id), self.get_encoding(wave_id),
                        (self.get_compression(wave_id) == constants.COMPRESSION_PCM_16_BE)
                        )
                wave_object = wave_object_from_blam_sound_perm(blam_perm)

            # initiate a queued play of the sound
            if wave_object is None:
                return

            self._wave_objects[wave_id] = wave_object
            # ensure the play_objects queue, lock, and force_stop all exist
            self.get_play_objects(wave_id)
            self.get_player_lock(wave_id)
            self.get_force_stop(wave_id).set(False)

            if threaded:
                self.play_wave_object_threaded(wave_id)
            else:
                self.play_wave_object(wave_id)

        except Exception:
            print(format_exc())

    def stop_sound(self, wave_id=None):
        self._stop_play_objects(
            self.get_play_objects(wave_id),
            self.get_player_lock(wave_id),
            self.get_force_stop(wave_id),
            )

    def stop_all_sounds(self):
        self._stop_play_objects(
            self._merged_play_objects, 
            self._merged_player_lock,
            self._merged_force_stop,
            )
        for wave_id in self._play_objects_by_wave_ids.keys():
            self._stop_play_objects(
                self._play_objects_by_wave_ids.get(wave_id),
                self._player_locks_by_wave_ids.get(wave_id),
                self._force_stops_by_wave_ids.get(wave_id),
                )

    def play_wave_object_threaded(self, wave_id=None):
        play_thread = threading.Thread(
            target=self.play_wave_object, daemon=True,
            args=(wave_id or self.get_wave_id(), )
            )
        play_thread.start()
        return play_thread

    def play_wave_object(self, wave_id=None):
        wave_id      = wave_id or self.get_wave_id()
        wave_object  = self._wave_objects[wave_id]
        if wave_object is None:
            return

        play_objects = self.get_play_objects(wave_id)
        player_lock  = self.get_player_lock(wave_id)
        force_stop   = self.get_force_stop(wave_id)

        # create a spot at the end of the queue and wait our turn
        queue_id = 1
        with player_lock:
            queue_id = max(tuple(play_objects) + (0, )) + 1
            play_objects[queue_id] = None
            #print("%s ENTERED QUEUE" % queue_id)

        # wait till its our turn to play
        while play_objects:
            curr_po_id, curr_po = queue_id, None
            with player_lock:
                curr_po_id  = min(tuple(play_objects) + (queue_id, ))
                curr_po     = play_objects.get(curr_po_id)

            if curr_po_id != queue_id and curr_po is None:
                # sound that's supposed to play hasn't yet.
                # we'll wait a short time, but if it doesn't play
                # then we'll need to remove it to remove deadlock
                time.sleep(1)
                with player_lock:
                    curr_po_id  = min(tuple(play_objects) + (queue_id, ))
                    curr_po     = play_objects.get(curr_po_id)
                    if curr_po is None:
                        #print("%s KICKING %s FROM QUEUE" % (queue_id, curr_po_id))
                        play_objects.pop(curr_po_id, None)

            #print("%s SEES CURR PLAYING IS %s" % (queue_id, curr_po_id))
            if curr_po_id == queue_id:
                break
            elif curr_po_id > queue_id:
                # our place in line got removed by another thread
                # that decided we deadlocked. oh well, gotta return
                #print("%s KICKED OUT OF QUEUE. RETURNING" % queue_id)
                return
            elif curr_po and curr_po.is_playing():
                #print("%s WAITING ON %s" % (queue_id, curr_po_id))
                curr_po.wait_done()

            if force_stop:
                #print("%s FORCE STOPPED. RETURNING" % queue_id)
                return

        # only play if we're still queued(sounds weren't stopped)
        po = None
        with player_lock:
            #print("%s PLAYING" % queue_id)
            # play the sound and add to the queue for tracking
            po = play_objects[queue_id] = wave_object.play()

        # wait till sound is done, and then cleanup
        try:
            po.wait_done()
        finally:
            #print("%s DONE PLAYING" % queue_id)
            play_objects.pop(queue_id, None)

    def _stop_play_objects(self, play_objects, player_lock, force_stop):
        force_stop.set(True)
        play_objects_copy = dict(play_objects)
        play_objects.clear()
        for queue_id in play_objects_copy:
            try:
                play_objects_copy[queue_id].stop()
            except Exception:
                pass


class SoundTagPlayer(SoundPlayerBase):
    sound_data = None
    big_endian_pcm = False

    @property
    def pitch_ranges(self):
        try:
            return {
                i: pr for i, pr in enumerate(
                self.sound_data.pitch_ranges.STEPTREE
                )}
        except AttributeError:
            return {}
    @property
    def permutations(self):
        try:
            return {
                i: pr for i, pr in enumerate(
                self.get_pitch_range().permutations.STEPTREE
                )}
        except AttributeError:
            return {}

    def get_permutation(self, pr_index=None, perm_index=None):
        if perm_index is None:
            perm_index = self.permutation_index

        pr    = self.get_pitch_range(pr_index)
        perms = None if pr is None else pr.permutations.STEPTREE
        return (
            perms[perm_index]
            if pr and perm_index in range(len(perms))
            else None
            )

    def get_compression(self, wave_id=None):
        block = getattr(self.get_permutation(), "compression", None)
        comp  = None if block is None else constants.halo_1_compressions[block.data]
        return (
            comp if not comp in constants.PCM_FORMATS else
            constants.COMPRESSION_PCM_16_BE if self.big_endian_pcm else
            constants.COMPRESSION_PCM_16_LE
            )

    def get_sample_rate(self, wave_id=None):
        block = getattr(self.sound_data, "sample_rate", None)
        return None if block is None else constants.halo_1_sample_rates[block.data]

    def get_encoding(self, wave_id=None):
        block = getattr(self.sound_data, "encoding", None)
        return None if block is None else constants.halo_1_encodings[block.data]


class SoundSourcePlayer(SoundPlayerBase):
    sound_bank = None

    @property
    def pitch_ranges(self):
        try:
            prs = self.sound_bank.pitch_ranges
            return {i: prs[name] for i, name in enumerate(sorted(prs))}
        except AttributeError:
            return {}
    @property
    def permutations(self):
        try:
            perms = self.get_pitch_range().permutations
            return {i: perms[name] for i, name in enumerate(sorted(perms))}
        except AttributeError:
            return {}

    def get_permutation(self, pr_index=None, perm_index=None):
        if perm_index is None:
            perm_index = self.permutation_index

        perms = getattr(self.get_pitch_range(pr_index), "permutations", {})
        try:
            perm_name = list(sorted(perms))[perm_index]
        except IndexError:
            perm_name = None

        return perms.get(perm_name)

    def get_compression(self, wave_id=None):
        return getattr(self.get_permutation(), "compression", None)

    def get_sample_rate(self, wave_id=None):
        return getattr(self.get_permutation(), "sample_rate", None)

    def get_encoding(self, wave_id=None):
        return getattr(self.get_permutation(), "encoding", None)