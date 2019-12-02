from reclaimer.sounds import constants
from reclaimer.sounds.adpcm import decode_adpcm_samples


def calculate_sample_chunk_size(compression, chunk_size, encoding):
    if compression == constants.COMPRESSION_ADPCM:
        block_size = ADPCM_COMPRESSED_BLOCKSIZE
        if encoding == constants.ENCODING_STEREO:
            block_size *= 2

        chunk_size = min(max(chunk_size, block_size),
                         constants.MAX_SAMPLE_CHUNK_SIZE)
        chunk_size -= chunk_size % block_size

    elif chunk_size <= 0:
        chunk_size = constants.DEF_SAMPLE_CHUNK_SIZE

    elif chunk_size > constants.MAX_SAMPLE_CHUNK_SIZE:
        chunk_size = constants.MAX_SAMPLE_CHUNK_SIZE

    return chunk_size


class BlamProcessedSoundSamples:
    _samples = b''
    _sample_count = 0
    _compression = constants.COMPRESSION_NONE
    _encoding = constants.ENCODING_MONO
    def __init__(self, samples, sample_count, compression, encoding):
        self._samples = samples
        self._sample_count = sample_count
        self._compression = compression
        self._encoding = encoding

    @property
    def samples(self):
        return self._samples
    @property
    def sample_count(self):
        return self._sample_count
    @property
    def compression(self):
        return self._compression
    @property
    def encoding(self):
        return self._encoding

    def get_decompressed(self):
        if self.compression == constants.COMPRESSION_NONE:
            return self.samples
        elif self.compression == constants.COMPRESSION_ADPCM:
            channel_count = 2 if self.encoding == constants.ENCODING_STEREO else 1
            return decode_adpcm_samples(self.samples, channel_count)
        else:
            raise NotImplementedError("whoops, decompressing this isn't implemented.")


class BlamSoundPermutation:
    # permutation properties
    name = "unnamed"
    _source_sample_data = b''
    _source_sample_rate = constants.SAMPLE_RATE_22K
    _source_encoding = constants.ENCODING_MONO

    # processed properties
    _processed_sample_pieces = ()

    def __init__(self, samples=b'', sample_rate=constants.SAMPLE_RATE_22K,
                 encoding=constants.ENCODING_MONO, **kwargs):
        self.name = kwargs.get("name", self.name)
        self.load_samples(samples, sample_rate, encoding)

    @property
    def source_sample_data(self):
        return self._source_sample_data
    @property
    def source_encoding(self):
        return self._source_encoding
    @property
    def source_encoding(self):
        return self._source_encoding
    @property
    def processed_samples(self):
        return self._processed_sample_pieces

    def load_samples(self, samples, sample_rate, encoding):
        self._source_samples = samples
        self._source_sample_rate = sample_rate
        self._source_encoding = encoding
        self._processed_sample_pieces = []

    def process_samples(self, compression, sample_rate, chunk_size=0):
        chunk_size = calculate_sample_chunk_size(
            compression, chunk_size, encoding)

        source_samples = self.source_samples
        if sample_rate != self.source_sample_rate:
            # resample to the target sample rate
            pass

        self._processed_sample_pieces = []

    def get_concatenated(self, decompress=True):
        if decompress:
            samples = b''.join(p.get_decompressed() for p in self.processed_samples)
        elif self.processed_samples:
            # make sure we're able to combine samples without decompressing
            compression = self.processed_samples[0].compression
            for piece in self.processed_samples:
                if piece.compression != compression:
                    raise ValueError(
                        "Cannot combine differently compressed samples without decompressing.")
                elif piece.compression == constants.COMPRESSION_OGG:
                    raise ValueError(
                        "Cannot combine ogg samples without decompressing.")

            samples = b''.join(p.samples for p in self.processed_samples)
        else:
            samples = b''

        return samples
