#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path

from reclaimer.h2.util import split_raw_pointer
from reclaimer.sounds import constants
from reclaimer.sounds import util
from reclaimer.sounds.blam_sound_bank import BlamSoundBank, BlamSoundPitchRange
from reclaimer.sounds.blam_sound_permutation import BlamSoundPermutation
from reclaimer.sounds.blam_sound_samples import BlamSoundSamples


__all__ = ("extract_h1_sounds", "extract_h2_sounds", )


def extract_h1_sounds(tagdata, tag_path, **kw):
    do_write_wav = kw.get('write_wav', True)
    overwrite = kw.get('overwrite', True)
    decompress = kw.get('decode_adpcm', True)
    pcm_is_big_endian = kw.get('byteswap_pcm_samples', False)
    tagpath_base = Path(kw['out_dir']).joinpath(Path(tag_path).with_suffix(""))

    encoding = tagdata.encoding.data
    channels = constants.channel_counts.get(encoding, 1)
    sample_rate = constants.halo_1_sample_rates.get(
        tagdata.sample_rate.data, 0)
    compression = constants.halo_1_compressions.get(
        tagdata.compression.data, constants.COMPRESSION_UNKNOWN)

    # make a BlamSoundBank to store all our sound data
    sound_bank = BlamSoundBank()
    sound_bank.split_into_smaller_chunks = tagdata.flags.split_long_sound_into_permutations
    sound_bank.split_to_adpcm_blocksize = tagdata.flags.fit_to_adpcm_blocksize
    sound_bank.sample_rate = sample_rate
    sound_bank.compression = compression
    sound_bank.encoding = encoding

    same_pr_names = {}
    for i, pr in enumerate(tagdata.pitch_ranges.STEPTREE):
        # determine a usable name for this pitch range
        pr_name = util.BAD_PATH_CHAR_REMOVAL.sub("_", pr.name.strip())
        if not pr_name:
            pr_name = str(i)

        same_pr_names[pr_name] = same_pr_names.get(pr_name, -1) + 1
        if same_pr_names[pr_name]:
            pr_name += "_%s" % same_pr_names[pr_name]

        # make a BlamPitchRange to store all the permutations
        sound_bank.pitch_ranges[pr_name] = BlamSoundPitchRange()

        same_names_permlists = {}
        unchecked_perms = set(range(len(pr.permutations.STEPTREE)))

        perm_indices = list(
            range(min(pr.actual_permutation_count, len(unchecked_perms))))
        if not perm_indices:
            perm_indices = set(unchecked_perms)

        playback_speed = 1.0
        if pr.natural_pitch > 0:
            playback_speed = 1 / pr.natural_pitch

        while perm_indices:
            # loop over all of the actual permutation indices and combine
            # the permutations they point to into a list with a shared name.
            # we do this so we can combine the permutations together into one.
            for j in perm_indices:
                perm = pr.permutations.STEPTREE[j]
                compression = perm.compression.enum_name
                name = perm.name if perm.name else str(j)
                permlist = same_names_permlists.get(name, [])
                same_names_permlists[name] = permlist

                while j in unchecked_perms:
                    perm = pr.permutations.STEPTREE[j]
                    if compression != perm.compression.enum_name:
                        # cant combine when compression is different
                        break

                    unchecked_perms.remove(j)
                    permlist.append(perm)

                    j = perm.next_permutation_index
            perm_indices = set(unchecked_perms)

        for name, permlist in same_names_permlists.items():
            blam_permutation = BlamSoundPermutation(
                sample_rate=sample_rate, encoding=encoding)
            sound_bank.pitch_ranges[pr_name].permutations[name] = blam_permutation

            for perm in permlist:
                sample_data = perm.samples.data
                if perm.compression.enum_name == "ogg":
                    # not actually a sample count. fix struct field name
                    compression = constants.COMPRESSION_OGG
                    sample_count = perm.ogg_sample_count // 2
                elif perm.compression.enum_name == "none":
                    compression = (constants.COMPRESSION_PCM_16_BE
                                   if pcm_is_big_endian else
                                   constants.COMPRESSION_PCM_16_LE)
                    sample_count = len(sample_data) // 2
                elif perm.compression.enum_name == "xbox_adpcm":
                    compression = constants.COMPRESSION_XBOX_ADPCM
                    sample_count = (
                        (constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2) *
                        (len(sample_data) // constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE))
                elif perm.compression.enum_name == "ima_adpcm":
                    compression = constants.COMPRESSION_IMA_ADPCM
                    sample_count = (
                        (constants.IMA_ADPCM_DECOMPRESSED_BLOCKSIZE // 2) *
                        (len(sample_data) // constants.IMA_ADPCM_COMPRESSED_BLOCKSIZE))
                else:
                    print("Unknown audio compression type:", perm.compression.data)
                    continue

                sample_count = sample_count // channels
                blam_permutation.processed_samples.append(
                    BlamSoundSamples(
                        sample_data, sample_count, compression,
                        int(round(sample_rate * playback_speed)),
                        encoding, perm.mouth_data.data)
                    )

    if do_write_wav:
        sound_bank.export_to_directory(
            tagpath_base, overwrite, False, decompress)
    else:
        return sound_bank


def get_sound_name(import_names, index):
    if index < 0 or index >= len(import_names):
        return ""
    return import_names[index].string


def extract_h2_sounds(tagdata, tag_path, **kw):
    # TODO: Make this multiply the sample rate by the natural pitch

    halo_map = kw.get('halo_map')
    if not halo_map:
        print("Cannot run this function on tags.")
        return

    do_write_wav = kw.get('write_wav', True)
    overwrite = kw.get('overwrite', True)
    decompress = kw.get('decode_adpcm', True)
    tagpath_base = Path(kw['out_dir']).joinpath(Path(tag_path).with_suffix(""))

    ugh__meta = halo_map.ugh__meta
    if ugh__meta is None:
        return "    No sound_cache_file_gestalt to read sounds from."

    import_names = ugh__meta.import_names.STEPTREE
    pitch_ranges = ugh__meta.pitch_ranges.STEPTREE
    permutations = ugh__meta.permutations.STEPTREE
    perm_chunks  = ugh__meta.permutation_chunks.STEPTREE

    same_pr_names = {}

    encoding = tagdata.encoding.data
    sample_rate = constants.halo_2_sample_rates.get(
        tagdata.sample_rate.data, 0)
    compression = constants.halo_2_compressions.get(
        tagdata.compression.data, constants.COMPRESSION_UNKNOWN)

    if encoding == constants.ENCODING_CODEC:
        compression = constants.COMPRESSION_UNKNOWN

    if tagdata.encoding.enum_name == "codec":
        pass # return "    CANNOT YET EXTRACT THIS FORMAT."
        '''
        The codec format seems to be encoded with wmaudio2.

        Bytes:
            0-31
                Two nearly identical GUIDs, with the second one specifying in
                its first 2 bytes that the audio data is encoded with wmaudio2.
            32-39
                Unknown, but always seems to be 01 00 00 00  00 00 00 00
            40-43
                Number of blocks of data(same value found in the header below)
            44-55
                Unknown, but I think it always seems to be the same.
            56-87
                wav_format header struct. sig is "ZYU\x00" instead of "fmt ",
                length is 28 instead of 20, and fmt is(always?) 0x0161,
                which is the format code for wmaudio2.
                channels, sample_rate, byte_rate, block_align, and
                bits_per_sample all seem to be set properly. the value
                for block_align is the same as bytes 40-43
            88-91
                Unknown. Might be something to specify the data length?

            Everything after this appears to be audio data.
        '''

    # get the pitch range indices to iterate over
    pr_index = tagdata.pitch_range_index
    pr_count = min(tagdata.pitch_range_count, len(pitch_ranges) - pr_index)
    if pr_index < 0 or pr_count < 0:
        # nothing to extract
        return

    # make a BlamSoundBank to store all our sound data
    sound_bank = BlamSoundBank()
    sound_bank.split_into_smaller_chunks = tagdata.flags.split_long_sound_into_permutations
    sound_bank.split_to_adpcm_blocksize = tagdata.flags.fit_to_adpcm_blocksize
    sound_bank.sample_rate = sample_rate
    sound_bank.compression = compression
    sound_bank.encoding = encoding

    for i in range(pr_index, pr_index + pr_count):
        pr = pitch_ranges[i]
        pr_name = get_sound_name(import_names, pr.import_name_index)
        pr_name = util.BAD_PATH_CHAR_REMOVAL.sub(
            "_", pr_name).strip().replace('|', ' ')
        if not pr_name:
            pr_name = str(i)

        same_pr_names[pr_name] = same_pr_names.get(pr_name, -1) + 1
        if same_pr_names[pr_name]:
            pr_name += "_%s" % same_pr_names[pr_name]

        # make a BlamPitchRange to store all the permutations
        sound_bank.pitch_ranges[pr_name] = BlamSoundPitchRange()

        # get the permutation indices to iterate over
        perm_index = pr.first_permutation
        perm_count = min(pr.permutation_count, len(permutations) - perm_index)
        if perm_index < 0 or perm_count < 0:
            continue

        for j in range(perm_index, perm_index + perm_count):
            perm = permutations[j]
            perm_name = get_sound_name(
                import_names, perm.import_name_index).replace('|', ' ')
            if not perm_name: perm_name = str(j)

            blam_permutation = BlamSoundPermutation(
                sample_rate=sample_rate, encoding=encoding)
            sound_bank.pitch_ranges[pr_name].permutations[perm_name] = blam_permutation

            # get the chunk indices to iterate over
            chunk_index = perm.first_chunk
            chunk_count = min(perm.chunk_count, len(perm_chunks) - chunk_index)
            if chunk_index < 0 or chunk_count < 0:
                continue

            for k in range(chunk_index, chunk_index + chunk_count):
                ptr, map_name = split_raw_pointer(perm_chunks[k].pointer)
                this_map = halo_map
                if map_name != "local":
                    this_map = halo_map.maps.get(map_name)

                if this_map is None or this_map.map_data is None:
                    continue

                this_map.map_data.seek(ptr)
                blam_permutation.processed_samples.append(
                    BlamSoundSamples(
                        this_map.map_data.read(perm_chunks[k].size),
                        0, compression, sample_rate, encoding)
                    )

    if do_write_wav:
        sound_bank.export_to_directory(
            tagpath_base, overwrite, False, decompress)
    else:
        return sound_bank
