import os

from traceback import format_exc

from reclaimer.sounds.blam_sound_permutation import BlamSoundPermutation
from reclaimer.sounds import constants, ogg


class BlamSoundPitchRange:
    _permutations = ()

    def __init__(self):
        self._permutations = {}

    @property
    def permutations(self):
        return self._permutations

    def partition_samples(
            self, compression=constants.COMPRESSION_PCM_16_LE,
            sample_rate=None,
            sample_chunk_size=constants.MAX_SAMPLE_CHUNK_SIZE):
        for perm in self.permutations.values():
            perm.partition_samples(
                compression, sample_rate, sample_chunk_size)

    def generate_mouth_data(self):
        for perm in self.permutations.values():
            perm.generate_mouth_data()

    def compress_samples(
            self, compression=constants.COMPRESSION_PCM_16_LE,
            sample_rate=None, encoding=None, vorbis_bitrate_info=None):
        for perm in self.permutations.values():
            perm.compress_samples(compression, sample_rate, encoding,
                                  vorbis_bitrate_info)

    def regenerate_source(self):
        for perm in self.permutations.values():
            perm.regenerate_source()

    @staticmethod
    def create_from_directory(directory):
        try:
            new_pitch_range = BlamSoundPitchRange()
            new_pitch_range.import_from_directory(directory)
            if not new_pitch_range.permutations:
                new_pitch_range = None
        except Exception:
            print(format_exc())
            new_pitch_range = None

        return new_pitch_range

    def export_to_directory(self, directory, overwrite=False,
                            export_source=True, decompress=True):
        for name, perm in self.permutations.items():
            perm.export_to_file(
                os.path.join(directory, name), overwrite,
                export_source, decompress)

    def import_from_directory(self, directory, clear_existing=True,
                              replace_existing=True):
        if clear_existing:
            self.permutations.clear()

        for root, _, files in os.walk(directory):
            # import each sound file to a new sound permutation
            for filename in files:
                if os.path.splitext(filename)[1].lower() != ".wav":
                    # only import wav files
                    continue

                name_key = filename.lower().strip()
                perm = BlamSoundPermutation.create_from_file(
                    os.path.join(root, filename))

                if perm and (replace_existing or
                             name_key not in self.permutations):
                    self.permutations[name_key] = perm

            # only loop over the files
            break


class BlamSoundBank:
    # processing settings
    encoding = constants.ENCODING_MONO
    compression = constants.COMPRESSION_PCM_16_LE
    sample_chunk_size = constants.DEF_SAMPLE_CHUNK_SIZE
    sample_rate = constants.SAMPLE_RATE_22K
    split_into_smaller_chunks = True
    split_to_adpcm_blocksize = True
    generate_mouth_data = False

    vorbis_bitrate_info = None

    _pitch_ranges = ()

    def __init__(self):
        self._pitch_ranges = {}
        self.vorbis_bitrate_info = ogg.VorbisBitrateInfo()

    @property
    def pitch_ranges(self):
        return self._pitch_ranges

    def partition_samples():
        for pitch_range in self.pitch_ranges.values():
            pitch_range.partition_samples(
                compression, sample_rate, sample_chunk_size)

    def generate_mouth_data(self):
        for pitch_range in self.pitch_ranges.values():
            pitch_range.generate_mouth_data()

    def compress_samples(self):
        for pitch_range in self.pitch_ranges.values():
            pitch_range.compress_samples(
                self.compression, self.sample_rate, self.encoding,
                self.vorbis_bitrate_info)

    def regenerate_source(self):
        for pitch_range in self.pitch_ranges.values():
            pitch_range.regenerate_source()

    @staticmethod
    def create_from_directory(directory, *args, **kwargs):
        try:
            new_sound_bank = BlamSoundBank(*args, **kwargs)
            new_sound_bank.import_from_directory(directory)
            if not new_sound_bank.pitch_ranges:
                new_sound_bank = None
        except Exception:
            print(format_exc())
            new_sound_bank = None

        return new_sound_bank

    def export_to_directory(self, directory, overwrite=False,
                            export_source=True, decompress=True):
        for name, pitch_range in self.pitch_ranges.items():
            if len(self.pitch_ranges) > 1:
                pitch_directory = os.path.join(directory, name)
            else:
                pitch_directory = directory

            pitch_range.export_to_directory(
                pitch_directory, overwrite, export_source, decompress)

    def import_from_directory(self, directory, clear_existing=True,
                              merge_same_names=False):
        if clear_existing:
            self.pitch_ranges.clear()

        # try to load default pitch range in sound root
        default_pitch_range = BlamSoundPitchRange.create_from_directory(
            directory)

        # try to load default from a directory named default as well
        default_dir_pitch_range = BlamSoundPitchRange.create_from_directory(
            os.path.join(directory, constants.DEFAULT_PITCH_RANGE_NAME))

        # either update the root default pitch ranges with the
        # other, or replace it with the directory one
        if default_dir_pitch_range:
            if default_pitch_range:
                default_pitch_range.permutations.update(
                    default_dir_pitch_range.permutations)
            else:
                default_pitch_range = default_dir_pitch_range

        # merge the default pitch range into this sound bank
        if default_pitch_range:
            name_key = constants.DEFAULT_PITCH_RANGE_NAME
            if self.pitch_ranges.get(name_key) is None:
                self.pitch_ranges[name_key] = default_pitch_range
            elif merge_same_names:
                self.pitch_ranges[name_key].permutations.update(
                    default_pitch_range.permutations)

        for root, dirs, _ in os.walk(directory):
            for dirname in dirs:
                name_key = dirname.lower().strip()
                if name_key == constants.DEFAULT_PITCH_RANGE_NAME:
                    # skip default pitch range(we took care of it above)
                    continue

                pitch_range = BlamSoundPitchRange.create_from_directory(
                    os.path.join(root, dirname))

                # merge the pitch range into this sound bank
                if pitch_range is not None:
                    if self.pitch_ranges.get(name_key) is None:
                        self.pitch_ranges[name_key] = pitch_range
                    elif merge_same_names:
                        self.pitch_ranges[name_key].permutations.update(
                            pitch_range.permutations)

            # only looping over the first level directories
            break
