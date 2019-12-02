import os
import re

from traceback import format_exc
from supyr_struct.defs.audio.wav import wav_def
from reclaimer.sounds.blam_sound_permutation import BlamSoundPermutation
from reclaimer.sounds import constants

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


class BlamSoundPitchRange:
    name = "default"
    _permutations = ()

    def __init__(self, ):
        self._permutations = {}

    @property
    def permutations(self):
        return self._permutations

    def process_samples(
            self, compression=constants.COMPRESSION_NONE,
            sample_rate=constants.SAMPLE_RATE_22K,
            sample_chunk_size=constants.MAX_SAMPLE_CHUNK_SIZE):
        for perm in self.permutations.values():
            perm.process_samples(
                compression, sample_rate, sample_chunk_size)


class BlamSoundBank:
    # processing settings
    encoding = constants.ENCODING_MONO
    compression = constants.COMPRESSION_NONE
    sample_chunk_size = constants.DEF_SAMPLE_CHUNK_SIZE
    sample_rate = constants.SAMPLE_RATE_22K
    split_into_smaller_chunks = True
    split_to_adpcm_blocksize = True

    _pitch_ranges = ()

    def __init__(self, ):
        self._pitch_ranges = {}

    @property
    def pitch_ranges(self):
        return self._pitch_ranges

    def process_samples(self):
        for pitch_range in self.permutations.values():
            pitch_range.process_samples(
                self.compression, self.sample_rate, self.sample_chunk_size)


def write_blam_sound_bank_permutation_list(
        permlist, filepath_base, sample_rate, channels=1, overwrite=True):
    wav_file = wav_def.build()

    for i in range(len(permlist)):
        compression, samples = permlist[i]
        filepath = filepath_base
        if not samples:
            continue

        if len(permlist) > 1: filepath += "__%s" % i

        is_container_format = compression in (
            constants.COMPRESSION_OGG, constants.COMPRESSION_WMA,
            constants.COMPRESSION_UNKNOWN,
            )

        if compression == constants.COMPRESSION_OGG:
            filepath += ".ogg"
        elif compression == constants.COMPRESSION_WMA:
            filepath += ".wma"
        elif compression == constants.COMPRESSION_UNKNOWN:
            filepath += ".bin"
        else:
            filepath += ".wav"

        filepath = BAD_PATH_CHAR_REMOVAL.sub("_", filepath)

        if not overwrite and os.path.isfile(filepath):
            continue

        if is_container_format:
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
            if compression == constants.COMPRESSION_NONE:
                wav_fmt.fmt.set_to('pcm')
                wav_fmt.block_align = 2 * wav_fmt.channels
            else:
                wav_fmt.fmt.set_to('ima_adpcm')
                wav_fmt.block_align = constants.ADPCM_COMPRESSED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(
                    wav_fmt.byte_rate *
                    (constants.ADPCM_COMPRESSED_BLOCKSIZE /
                     constants.ADPCM_DECOMPRESSED_BLOCKSIZE))

            wav_file.data.wav_data.audio_data = samples
            wav_file.data.wav_data.audio_data_size = samples_len
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)

