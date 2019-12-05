import os
import re

from array import array
from traceback import format_exc

from reclaimer.sounds import constants
from reclaimer.sounds import util
from reclaimer.sounds.adpcm import decode_adpcm_samples

from supyr_struct.defs.audio.wav import wav_def

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


class BlamSoundSamples:
    _samples = b''
    _sample_count = 0
    _compression = constants.COMPRESSION_PCM_16_LE
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

    def get_decompressed(self, target_compression):
        assert target_compression in constants.PCM_FORMATS

        if self.compression == constants.COMPRESSION_ADPCM:
            # decompress adpcm to 16bit pcm
            samples = decode_adpcm_samples(
                self.samples, constants.channel_counts.get(self.encoding, 1))
            curr_compression = constants.ADPCM_DECOMPRESSED_ENDIANNESS
        elif self.compression in constants.PCM_FORMATS:
            # samples are decompressed. use as-is
            curr_compression = self.compression
            samples = self.samples
        else:
            raise NotImplementedError("whoops, decompressing this isn't implemented.")

        if curr_compression != target_compression:
            samples = util.convert_pcm_to_pcm(
                samples, curr_compression, target_compression)

        return samples


class BlamSoundPermutation:
    # permutation properties
    name = "unnamed"
    _source_sample_data = b''
    _source_sample_rate = constants.SAMPLE_RATE_22K
    _source_encoding = constants.ENCODING_MONO

    # processed properties
    _processed_samples = ()

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
        return self._processed_samples
    @property
    def compression(self):
        try:
            return self.processed_samples[0].compression
        except Exception:
            return constants.COMPRESSION_UNKNOWN
    @property
    def encoding(self):
        try:
            return self.processed_samples[0].encoding
        except Exception:
            return constants.ENCODING_UNKNOWN

    def load_samples(self, samples, sample_rate, encoding):
        self._source_samples = samples
        self._source_sample_rate = sample_rate
        self._source_encoding = encoding
        self._processed_samples = []

    def process_samples(self, compression, sample_rate, chunk_size=0):
        chunk_size = util.calculate_sample_chunk_size(
            compression, chunk_size, encoding)

        source_samples = self.source_samples
        if sample_rate != self.source_sample_rate:
            # resample to the target sample rate
            pass

        self._processed_samples = []

    def get_concatenated(self, target_compression=None):
        if target_compression is None:
            target_compression = self.compression

        if target_compression != self.compression:
            # decompress processed samples to the target compression
            samples = b''.join(p.get_decompressed(target_compression)
                               for p in self.processed_samples)
        else:
            # join samples without decompressing

            compression = self.compression
            # make sure we're able to combine samples without decompressing
            for piece in self.processed_samples:
                if piece.compression != compression:
                    raise ValueError(
                        "Cannot combine differently compressed samples without decompressing.")
                elif piece.compression == constants.COMPRESSION_OGG:
                    raise ValueError(
                        "Cannot combine ogg samples without decompressing.")

            samples = b''.join(p.samples for p in self.processed_samples)

        return samples

    def export_to_file(filepath_base, export_source=True, decompress=True):
        perm_chunks = []
        encoding = self.encoding
        if export_source and self.source_sample_data:
            # export the source data
            perm_chunks.append(
                (compression, self.source_encoding, self.source_sample_data)
                )
        elif self.processed_samples:
            # concatenate processed samples if source samples don't exist.
            # also, if compression is ogg, we have to decompress
            if decompress or self.compression == constants.COMPRESSION_OGG:
                compression = constants.COMPRESSION_PCM_16_LE
            else:
                compression = self.compression

            try:
                samples = self.get_concatenated(compression)
                if samples:
                    perm_chunks.append((compression, self.encoding, samples))
            except Exception:
                perm_chunks.extend(
                    (piece.compression, piece.encoding, piece.samples)
                    for piece in self.processed_samples
                    )

        i = -1
        wav_file = wav_def.build()
        for compression, encoding, samples in perm_chunks:
            i += 1
            filepath = BAD_PATH_CHAR_REMOVAL.sub("_", filepath_base)

            if len(perm_chunks) > 1:
                filepath += "__%s" % i

            # figure out if the sample data is already encapsulated in a
            # container, or if it'll need to be encapsulated in a wav file.
            is_container_format = True
            if compression == constants.COMPRESSION_OGG:
                filepath += ".ogg"
            elif compression == constants.COMPRESSION_WMA:
                filepath += ".wma"
            elif compression == constants.COMPRESSION_UNKNOWN:
                filepath += ".bin"
            else:
                is_container_format = False
                filepath += ".wav"

            if not samples or (not overwrite and os.path.isfile(filepath)):
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

                continue

            wav_file.filepath = filepath

            wav_fmt = wav_file.data.format
            wav_fmt.fmt.set_to('pcm')
            wav_fmt.channels = constants.encoding_channels.get(encoding, 1)
            wav_fmt.sample_rate = sample_rate

            samples_len = len(samples)
            if compression in constants.PCM_FORMATS:
                # one of the uncompressed pcm formats
                if util.is_big_endian_pcm(compression):
                    samples = util.convert_pcm_to_pcm(
                        samples, compression,
                        util.change_pcm_endianness(compression))

                sample_width = constants.sample_widths[compression]
                wav_fmt.bits_per_sample = sample_width * 8
                wav_fmt.block_align = sample_width * wav_fmt.channels
                wav_fmt.byte_rate = wav_fmt.sample_rate * wav_fmt.block_align
            elif compression == constants.COMPRESSION_ADPCM:
                # 16bit adpcm
                wav_fmt.fmt.set_to('ima_adpcm')
                wav_fmt.bits_per_sample = 16
                wav_fmt.block_align = constants.ADPCM_COMPRESSED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(
                    (wav_fmt.sample_rate * wav_fmt.block_align) /
                     constants.ADPCM_DECOMPRESSED_BLOCKSIZE)
            else:
                print("Unknown compression method:", compression)
                continue

            wav_file.data.wav_data.audio_data = samples
            wav_file.data.wav_data.audio_data_size = samples_len
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)
