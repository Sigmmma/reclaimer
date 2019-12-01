import os
import re

from traceback import format_exc
from supyr_struct.defs.audio.wav import wav_def
from reclaimer.sounds.adpcm import ADPCM_BLOCKSIZE, PCM_BLOCKSIZE
from reclaimer.sounds.blam_sound_permutation import BlamSoundPermutation,\
     DEF_SAMPLE_CHUNK_SIZE

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


class BlamSoundPitchRange:
    name = "default"

    natural_pitch = 1.0
    pitch_bend_lower = 0.0
    pitch_bend_upper = 1.0

    _permutations = ()

    def __init__(self, ):
        self._permutations = {}

    @property
    def permutations(self): return self._permutations


class BlamSoundBank:
    # TODO: Finish putting sound processing settings in here

    # processing settings
    sample_chunk_size = DEF_SAMPLE_CHUNK_SIZE
    split_into_smaller_chunks = True
    split_to_adpcm_blocksize = True

    _pitch_ranges = ()

    def __init__(self, ):
        self._pitch_ranges = {}

    @property
    def pitch_ranges(self): return self._pitch_ranges


def write_blam_sound_bank_permutation_list(
        permlist, filepath_base, sample_rate, channels=1, overwrite=True):
    wav_file = wav_def.build()

    for i in range(len(permlist)):
        encoding, samples = permlist[i]
        filepath = filepath_base
        if not samples:
            continue

        if len(permlist) > 1: filepath += "__%s" % i

        if encoding in ("ogg", "wma"):
            filepath += ".%s" % encoding
        elif not encoding:
            filepath += ".bin"
        else:
            filepath += ".wav"

        filepath = BAD_PATH_CHAR_REMOVAL.sub("_", filepath)

        if not overwrite and os.path.isfile(filepath):
            continue

        if encoding in ("ogg", "wma") or not encoding:
            try:
                folderpath = os.path.dirname(filepath)
                # If the path doesnt exist, create it
                if not os.path.exists(folderpath):
                    os.makedirs(folderpath)

                with open(filepath, "wb") as f:
                    f.write(samples)
            except Exception:
                print(format_exc())
        else:
            wav_file.filepath = filepath

            wav_fmt = wav_file.data.format
            wav_fmt.channels = channels
            wav_fmt.sample_rate = sample_rate
            wav_fmt.bits_per_sample = 16
            wav_fmt.byte_rate = ((wav_fmt.sample_rate *
                                  wav_fmt.bits_per_sample *
                                  wav_fmt.channels) // 8)

            samples_len = len(samples)
            if encoding == "none":
                wav_fmt.fmt.set_to('pcm')
                wav_fmt.block_align = 2 * wav_fmt.channels
            else:
                wav_fmt.fmt.set_to('ima_adpcm')
                wav_fmt.block_align = XBOX_ADPCM_ENCODED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(wav_fmt.byte_rate *
                                        XBOX_ADPCM_ENCODED_BLOCKSIZE/XBOX_ADPCM_DECODED_BLOCKSIZE/2)

            wav_file.data.wav_data.audio_data = samples
            wav_file.data.wav_data.audio_data_size = samples_len
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)

