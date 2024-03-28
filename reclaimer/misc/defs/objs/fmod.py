#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from supyr_struct.tag import Tag

FMOD_BANK_HEADER_SIZE  = 60
FMOD_SAMPLE_CHUNK_SIZE = 16
FMOD_SAMPLE_DATA_ALIGN = 32

class FModSoundBankTag(Tag):

    def set_pointers(self, offset=0):
        header  = self.data.header
        samples = self.data.samples
        names   = self.data.names
        if len(samples) != len(names):
            raise ValueError("Number of samples does not match number of names.")

        header.sample_count = len(samples)
        sample_headers_size = sample_names_size = sample_data_size = 0

        for sample in samples:
            sample_headers_size += sample.header.binsize + sample.chunks.binsize
            sample.header.data_qword_offset = sample_data_size
            sample_size = (
                len(sample.sample_data) + FMOD_SAMPLE_CHUNK_SIZE - 1
                ) // FMOD_SAMPLE_CHUNK_SIZE

            sample_data_size += sample_size

        sample_names_size += 4*header.sample_count # string offset sizes
        for name in names:
            name.offset = sample_names_size
            sample_names_size += len(name.name) + 1 # add 1 for null terminator

        sample_data_off = FMOD_BANK_HEADER_SIZE + sample_headers_size + sample_names_size
        sample_name_padding = (
            (FMOD_SAMPLE_DATA_ALIGN - sample_data_off % FMOD_SAMPLE_DATA_ALIGN)
            ) % FMOD_SAMPLE_DATA_ALIGN
        header.sample_headers_size  = sample_headers_size
        header.sample_names_size    = sample_names_size + sample_name_padding
        header.sample_data_size     = sample_data_size*FMOD_SAMPLE_CHUNK_SIZE

    def serialize(self, *args, **kwargs):
        self.set_pointers()
        super().serialize(*args, **kwargs)