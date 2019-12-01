
COMPRESSION_NONE = 0
COMPRESSION_ADPCM = 1
COMPRESSION_OGG = 2
COMPRESSION_WMA = 3

DEF_SAMPLE_CHUNK_SIZE = 0x10000
MAX_SAMPLE_CHUNK_SIZE = 0x400000
MAX_MOUTH_DATA   = 0x2000


class BlamSoundPermutation:
    # permutation properties
    name = "unnamed"
    raw_sample_data = b''
    skip_fraction = 0.0
    sample_rate = 22050
    gain = 1.0

    # processed properties
    sample_pieces = ()
    _compression = COMPRESSION_NONE

    def __init__(self):
        self.sample_pieces = []

    @property
    def sample_count(self):
        return len(raw_sample_data) // 2

    @property
    def compression(self):
        return self.compression == COMPRESSION_NONE

    def generate_sample_pieces(
            self, compression=COMPRESSION_NONE,
            split_into_smaller_chunks=True,
            split_to_adpcm_blocksize=True,
            sample_chunk_size=DEF_SAMPLE_CHUNK_SIZE):

        self.sample_pieces = []
        self._compression = compression
