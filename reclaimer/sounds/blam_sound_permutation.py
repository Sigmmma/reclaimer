#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path
from traceback import format_exc

from reclaimer.sounds import constants, util, blam_sound_samples
from supyr_struct.defs.audio.wav import wav_def
from supyr_struct.util import is_path_empty


class BlamSoundPermutation:
    name = ""

    # permutation properties
    _source_sample_data = b''
    _source_compression = constants.COMPRESSION_PCM_16_LE
    _source_sample_rate = constants.SAMPLE_RATE_22K
    _source_encoding = constants.ENCODING_MONO

    # processed properties
    _processed_samples = ()

    def __init__(self, sample_data=b'',
                 compression=constants.COMPRESSION_PCM_16_LE,
                 sample_rate=constants.SAMPLE_RATE_22K,
                 encoding=constants.ENCODING_MONO, **kwargs):
        self.load_source_samples(
            sample_data, compression, sample_rate, encoding)

    @property
    def source_sample_data(self):
        return self._source_sample_data
    @property
    def source_compression(self):
        return self._source_compression
    @property
    def source_sample_rate(self):
        return self._source_sample_rate
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
            return self._source_compression
    @property
    def sample_rate(self):
        try:
            return self.processed_samples[0].sample_rate
        except Exception:
            return self._source_sample_rate
    @property
    def encoding(self):
        try:
            return self.processed_samples[0].encoding
        except Exception:
            return self._source_encoding

    def load_source_samples(self, sample_data, compression,
                            sample_rate, encoding):
        self._source_sample_data = sample_data
        self._source_compression = compression
        self._source_sample_rate = sample_rate
        self._source_encoding = encoding
        self._processed_samples = []

    def partition_samples(self, target_compression=None,
                          target_sample_rate=None, target_encoding=None,
                          chunk_size=None, **compressor_kwargs):
        if target_compression is None:
            target_compression = self.source_compression

        if target_sample_rate is None:
            target_sample_rate = self.source_sample_rate

        if target_encoding is None:
            target_encoding = self.source_encoding

        if self.source_compression == constants.COMPRESSION_OGG:
            raise NotImplementedError(
                "Cannot partition Ogg Vorbis samples.")
        elif (target_compression not in constants.PCM_FORMATS and
              target_compression != constants.COMPRESSION_IMA_ADPCM and
              target_compression != constants.COMPRESSION_XBOX_ADPCM and
              target_compression != constants.COMPRESSION_OGG):
            raise ValueError('Unknown compression type "%s"' % target_compression)
        elif target_encoding not in (constants.ENCODING_MONO,
                                     constants.ENCODING_STEREO):
            raise ValueError("Compression encoding must be mono or stereo.")
        elif target_sample_rate <= 0:
            raise ValueError("Sample rate must be greater than zero.")

        source_compression = self.source_compression
        source_sample_rate = self.source_sample_rate
        source_encoding = self.source_encoding
        source_sample_data = self.source_sample_data

        target_chunk_size = util.get_sample_chunk_size(
            target_compression, target_encoding, chunk_size)
        if (source_compression == target_compression and
            source_sample_rate == target_sample_rate and
            source_encoding == target_encoding and
            (source_compression in constants.PCM_FORMATS or
             source_compression == constants.COMPRESSION_IMA_ADPCM or
             source_compression == constants.COMPRESSION_XBOX_ADPCM)):
            # compressing to same settings and can split at target_chunk_size
            # because format has fixed compression ratio. recompression not
            # necessary. Just split source into pieces at target_chunk_size.

            source_chunk_size = target_chunk_size
        else:
            # decompress samples so we can partition to a
            # different compression/encoding/sample rate
            decompressor = blam_sound_samples.BlamSoundSamples(
                source_sample_data, 0, source_compression,
                source_sample_rate, source_encoding
                )
            source_compression = constants.DEFAULT_UNCOMPRESSED_FORMAT
            source_sample_rate = target_sample_rate
            source_encoding = target_encoding
            source_sample_data = decompressor.get_decompressed(
                source_compression, source_sample_rate, source_encoding)

            source_bytes_per_sample = util.get_block_size(
                source_compression, source_encoding)

            target_blocksize = util.get_block_size(
                target_compression, target_encoding)
            target_samples_per_block = util.get_samples_per_block(
                target_compression)

            target_blocks_per_chunk = target_chunk_size // target_blocksize
            target_samples_per_chunk = (target_samples_per_block *
                                        target_blocks_per_chunk)
            source_chunk_size = (source_bytes_per_sample *
                                 target_samples_per_chunk)

        self._processed_samples = []
        for i in range(0, len(source_sample_data), source_chunk_size):
            chunk = source_sample_data[i: i + source_chunk_size]
            sample_count = util.get_sample_count(
                chunk, source_compression, source_encoding)

            self.processed_samples.append(
                blam_sound_samples.BlamSoundSamples(
                    chunk, sample_count, source_compression,
                    source_sample_rate, source_encoding)
                )

    def generate_mouth_data(self):
        for samples in self.processed_samples:
            samples.generate_mouth_data()

    def compress_samples(self, compression, sample_rate=None, encoding=None,
                         chunk_size=None, **compressor_kwargs):
        self.partition_samples(
            compression, sample_rate, encoding,
            chunk_size, **compressor_kwargs)
        for samples in self.processed_samples:
            samples.compress(compression, sample_rate, encoding,
                             **compressor_kwargs)

    def get_concatenated_sample_data(self, target_compression=None,
                                     target_sample_rate=None,
                                     target_encoding=None):
        if target_compression is None:
            target_compression = self.source_compression

        if target_sample_rate is None:
            target_sample_rate = self.source_sample_rate

        if target_encoding is None:
            target_encoding = self.source_encoding

        assert target_encoding in constants.channel_counts

        if (target_compression != self.compression or
            target_sample_rate != self.sample_rate or
            target_encoding != self.encoding):
            # decompress processed samples to the target compression
            sample_data = b''.join(
                p.get_decompressed(
                    target_compression, target_sample_rate, target_encoding)
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

            sample_data = b''.join(p.sample_data for p in self.processed_samples)

        return sample_data

    def get_concatenated_mouth_data(self):
        return b''.join(p.mouth_data for p in self.processed_samples)

    def regenerate_source(self):
        '''
        Regenerates an uncompressed, concatenated audio stream
        from the compressed samples. Use when loading a sound tag
        for re-compression, re-sampling, or re-encoding.
        '''
        # always regenerate to constants.DEFAULT_UNCOMPRESSED_FORMAT
        # because, technically speaking, that is highest sample depth
        # we can ever possibly see in Halo CE.
        self._source_sample_data = self.get_concatenated_sample_data(
            constants.DEFAULT_UNCOMPRESSED_FORMAT,
            self.sample_rate, self.encoding)
        self._source_compression = constants.DEFAULT_UNCOMPRESSED_FORMAT
        self._source_sample_rate = self.sample_rate
        self._source_encoding = self.encoding

    @staticmethod
    def create_from_file(filepath):
        try:
            new_perm = BlamSoundPermutation()
            new_perm.import_from_file(filepath)
        except Exception:
            print(format_exc())
            new_perm = None

        return new_perm

    def export_to_file(self, filepath_base, overwrite=False,
                       export_source=True, decompress=True):
        perm_chunks = []
        encoding = self.encoding
        sample_rate = self.sample_rate
        if export_source and self.source_sample_data:
            # export the source data
            perm_chunks.append(
                (self.compression, self.source_encoding, self.source_sample_data)
                )
            sample_rate = self.source_sample_rate
        elif self.processed_samples:
            # concatenate processed samples if source samples don't exist.
            # also, if compression is ogg, we have to decompress
            compression = self.compression
            if decompress or compression == constants.COMPRESSION_OGG:
                compression = constants.COMPRESSION_PCM_16_LE

            try:
                sample_data = self.get_concatenated_sample_data(
                    compression, sample_rate, encoding)
                if sample_data:
                    perm_chunks.append((compression, self.encoding, sample_data))
            except Exception:
                print("Could not decompress permutation pieces. Concatenating.")
                perm_chunks.extend(
                    (piece.compression, piece.encoding, piece.sample_data)
                    for piece in self.processed_samples
                    )

        i = -1
        wav_file = wav_def.build()
        for compression, encoding, sample_data in perm_chunks:
            i += 1
            filepath = Path(util.BAD_PATH_CHAR_REMOVAL.sub("_", str(filepath_base)))

            if is_path_empty(filepath):
                filepath = Path("unnamed")

            if len(perm_chunks) > 1:
                filepath = filepath.parent.joinpath(filepath.stem + "__%s" % i)

            # figure out if the sample data is already encapsulated in a
            # container, or if it'll need to be encapsulated in a wav file.
            is_container_format = True
            if compression == constants.COMPRESSION_OGG:
                ext = ".ogg"
            elif compression == constants.COMPRESSION_WMA:
                ext = ".wma"
            elif compression == constants.COMPRESSION_UNKNOWN:
                ext = ".bin"
            else:
                is_container_format = False
                ext = ".wav"

            if filepath.suffix.lower() != ext:
                filepath = filepath.with_suffix(ext)

            if not sample_data or (not overwrite and filepath.is_file()):
                continue

            if is_container_format:
                try:
                    filepath.parent.mkdir(exist_ok=True, parents=True)
                    with filepath.open("wb") as f:
                        f.write(sample_data)
                except Exception:
                    print(format_exc())

                continue

            wav_file.filepath = filepath

            wav_fmt = wav_file.data.wav_format
            wav_chunks = wav_file.data.wav_chunks
            wav_chunks.append(case="data")
            data_chunk = wav_chunks[-1]

            wav_fmt.fmt.data = constants.WAV_FORMAT_PCM
            wav_fmt.channels = constants.channel_counts.get(encoding, 1)
            wav_fmt.sample_rate = sample_rate

            samples_len = len(sample_data)
            if compression in constants.PCM_FORMATS:
                # one of the uncompressed pcm formats
                if util.is_big_endian_pcm(compression):
                    sample_data = util.convert_pcm_to_pcm(
                        sample_data, compression,
                        util.change_pcm_endianness(compression))

                sample_width = constants.sample_widths[compression]
                wav_fmt.bits_per_sample = sample_width * 8
                wav_fmt.block_align = sample_width * wav_fmt.channels
                wav_fmt.byte_rate = wav_fmt.sample_rate * wav_fmt.block_align
            elif compression == constants.COMPRESSION_IMA_ADPCM:
                # 16bit adpcm
                wav_fmt.fmt.data = constants.WAV_FORMAT_IMA_ADPCM
                wav_fmt.bits_per_sample = 16
                wav_fmt.block_align = constants.IMA_ADPCM_COMPRESSED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(
                    (wav_fmt.sample_rate * wav_fmt.block_align /
                     (constants.IMA_ADPCM_DECOMPRESSED_BLOCKSIZE // 2))
                    )
            elif compression == constants.COMPRESSION_XBOX_ADPCM:
                # 16bit adpcm
                wav_fmt.fmt.data = constants.WAV_FORMAT_XBOX_ADPCM
                wav_fmt.bits_per_sample = 16
                wav_fmt.block_align = constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(
                    (wav_fmt.sample_rate * wav_fmt.block_align /
                     (constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2))
                    )
            else:
                print("Unknown compression method:", compression)
                continue

            data_chunk.data = sample_data
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)

    def import_from_file(self, filepath):
        filepath = Path(filepath)
        if not filepath.is_file():
            raise OSError('File "%s" does not exist. Cannot import.' % filepath)

        wav_file = wav_def.build(filepath=filepath)
        wav_header = wav_file.data.wav_header
        wav_format = wav_file.data.wav_format
        wav_chunks = wav_file.data.wav_chunks
        data_chunk = None
        for chunk in wav_chunks:
            if chunk.sig.enum_name == "data":
                data_chunk = chunk
                break

        if wav_header.riff_sig != wav_header.get_desc("DEFAULT", "riff_sig"):
            raise ValueError(
                "RIFF signature is invalid. Not a valid wav file.")
        elif wav_header.wave_sig != wav_header.get_desc("DEFAULT", "wave_sig"):
            raise ValueError(
                "WAVE signature is invalid. Not a valid wav file.")
        elif wav_format.sig != wav_format.get_desc("DEFAULT", "sig"):
            raise ValueError(
                "Format signature is invalid. Not a valid wav file.")
        elif data_chunk is None:
            raise ValueError("Data chunk not present. Not a valid wav file.")
        elif wav_format.fmt.data not in constants.ALLOWED_WAV_FORMATS:
            raise ValueError(
                'Invalid compression format "%s".' % wav_format.fmt.data)
        elif wav_format.channels not in (1, 2):
            raise ValueError(
                "Invalid number of channels. Must be 1 or 2, not %s." %
                wav_format.channels)
        elif wav_format.sample_rate == 0:
            raise ValueError(
                "Sample rate cannot be zero. Not a valid wav file")
        elif (wav_format.fmt.data == constants.WAV_FORMAT_PCM_FLOAT and
              wav_format.bits_per_sample != 32):
            raise ValueError(
                "Pcm float sample width must be 32, not %s." %
                wav_format.bits_per_sample)
        elif (wav_format.fmt.data == constants.WAV_FORMAT_PCM and
              wav_format.bits_per_sample not in (8, 16, 24, 32)):
            raise ValueError(
                "Pcm sample width must be 8, 16, 24, or 32, not %s." %
                wav_format.bits_per_sample)

        if data_chunk.data_size != len(data_chunk.data):
            print("Audio sample data length does not match available data "
                  "length. Sample data may be truncated.")

        if wav_format.block_align and (len(data_chunk.data) %
                                       wav_format.block_align):
            print("Audio sample data length not a multiple of block_align. "
                  "Sample data may be truncated.")

        if wav_format.channels == 2:
            encoding = constants.ENCODING_STEREO
        else:
            encoding = constants.ENCODING_MONO

        sample_data = data_chunk.data
        if wav_format.fmt.data == constants.WAV_FORMAT_PCM_FLOAT:
            sample_data = util.convert_pcm_float32_to_pcm_32(sample_data)
            compression = constants.COMPRESSION_PCM_32_LE
        else:
            sample_width = None
            if wav_format.fmt.data == constants.WAV_FORMAT_PCM:
                sample_width = wav_format.bits_per_sample // 8

            compression = constants.wav_format_mapping.get(
                (wav_format.fmt.data, sample_width))

        self.load_source_samples(
            sample_data, compression, wav_format.sample_rate, encoding)
