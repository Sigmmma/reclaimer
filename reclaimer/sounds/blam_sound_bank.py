import os

from reclaimer.sounds.blam_sound_permutation import BlamSoundPermutation
from reclaimer.sounds import constants


class BlamSoundPitchRange:
    _permutations = ()

    def __init__(self):
        self._permutations = {}

    @property
    def permutations(self):
        return self._permutations

    def process_samples(
            self, compression=constants.COMPRESSION_PCM_16_LE,
            sample_rate=constants.SAMPLE_RATE_22K,
            sample_chunk_size=constants.MAX_SAMPLE_CHUNK_SIZE):
        for perm in self.permutations.values():
            perm.process_samples(
                compression, sample_rate, sample_chunk_size)

    def export_to_directory(self, directory_base, overwrite=False,
                            export_source=True, decompress=True):
        for name, perm in self.permutations.items():
            perm.export_to_directory(
                os.path.join(directory_base, name), overwrite,
                export_source, decompress)


class BlamSoundBank:
    # processing settings
    encoding = constants.ENCODING_MONO
    compression = constants.COMPRESSION_PCM_16_LE
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

    def export_to_directory(self, directory_base, overwrite=False,
                            export_source=True, decompress=True):
        for name, pitch_range in self.pitch_ranges.items():
            if len(self.pitch_ranges) > 1:
                pitchpath_base = os.path.join(directory_base, name)
            else:
                pitchpath_base = directory_base

            pitch_range.export_to_directory(
                pitchpath_base, overwrite, export_source, decompress)
