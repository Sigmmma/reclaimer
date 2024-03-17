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

from reclaimer.sounds import blam_sound_samples, constants as const, ogg, util
from supyr_struct.defs.audio.wav import wav_def
from supyr_struct.util import is_path_empty


class BlamSoundPermutation:
    name = ""

    # permutation properties
    _source_filename    = ""
    _source_sample_data = b''
    _source_compression = const.COMPRESSION_PCM_16_LE
    _source_sample_rate = const.SAMPLE_RATE_22K
    _source_encoding    = const.ENCODING_MONO

    # processed properties
    _processed_samples = ()

    def __init__(self, sample_data=b'',
                 compression=const.COMPRESSION_PCM_16_LE,
                 sample_rate=const.SAMPLE_RATE_22K,
                 encoding=const.ENCODING_MONO, **kwargs):
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
    def source_filename(self):
        return self._source_filename

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
                            sample_rate, encoding, filename=""):
        self._source_sample_data = sample_data
        self._source_compression = compression
        self._source_sample_rate = sample_rate
        self._source_encoding    = encoding
        self._source_filename    = filename
        self._processed_samples  = []

    def partition_samples(self, target_compression=None,
                          target_sample_rate=None, target_encoding=None,
                          chunk_size=None, **compressor_kwargs):
        if target_compression is None:
            target_compression = self.source_compression

        if target_sample_rate is None:
            target_sample_rate = self.source_sample_rate

        if target_encoding is None:
            target_encoding = self.source_encoding

        if (target_compression not in const.PCM_FORMATS and
              target_compression != const.COMPRESSION_IMA_ADPCM and
              target_compression != const.COMPRESSION_XBOX_ADPCM and
              target_compression != const.COMPRESSION_OGG):
            raise ValueError('Unknown compression type "%s"' % target_compression)
        elif target_encoding not in (const.ENCODING_MONO,
                                     const.ENCODING_STEREO):
            raise ValueError("Compression encoding must be mono or stereo.")
        elif target_sample_rate <= 0:
            raise ValueError("Sample rate must be greater than zero.")

        source_compression = self.source_compression
        source_sample_rate = self.source_sample_rate
        source_encoding    = self.source_encoding
        source_sample_data = self.source_sample_data

        target_chunk_size = util.get_sample_chunk_size(
            target_compression, target_encoding, chunk_size)
        if (source_compression == target_compression and
            source_sample_rate == target_sample_rate and
            source_encoding == target_encoding and
            (source_compression in const.PCM_FORMATS or
             source_compression == const.COMPRESSION_IMA_ADPCM or
             source_compression == const.COMPRESSION_XBOX_ADPCM)):
            # compressing to same settings and can split at target_chunk_size
            # because format has fixed compression ratio. recompression not
            # necessary. Just split source into pieces at target_chunk_size.

            source_chunk_size = target_chunk_size
        else:
            # decompress samples so we can partition to a
            # different compression/encoding/sample rate
            source_compression = const.DEFAULT_UNCOMPRESSED_FORMAT
            source_sample_rate = target_sample_rate
            source_encoding    = target_encoding
            source_sample_data = self.decompress_source_samples(
                source_compression, source_sample_rate, source_encoding
                )

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

    def decompress_source_samples(self, compression, sample_rate, encoding):
        assert compression in const.PCM_FORMATS
        assert encoding in const.channel_counts

        # decompress samples so we can partition to a
        # different compression/encoding/sample rate
        decompressor = blam_sound_samples.BlamSoundSamples(
            self.source_sample_data, 0, self.source_compression,
            self.source_sample_rate, self.source_encoding
            )
        return decompressor.get_decompressed(
            compression, sample_rate, encoding
            )

    def get_concatenated_sample_data(self, target_compression=None,
                                     target_sample_rate=None,
                                     target_encoding=None):
        if target_compression is None:
            target_compression = self.source_compression

        if target_sample_rate is None:
            target_sample_rate = self.source_sample_rate

        if target_encoding is None:
            target_encoding = self.source_encoding

        assert target_encoding in const.channel_counts

        if (target_compression != self.compression or
            target_sample_rate != self.sample_rate or
            target_encoding    != self.encoding):
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
                elif piece.compression == const.COMPRESSION_OGG:
                    raise ValueError(
                        "Cannot combine ogg samples without decompressing.")

            sample_data = b''.join(p.sample_data for p in self.processed_samples)

        return sample_data

    def get_concatenated_mouth_data(self):
        return b''.join(p.mouth_data for p in self.processed_samples)

    def regenerate_source(
            self, compression=None, sample_rate=None, encoding=None
            ):
        '''
        Regenerates an uncompressed, concatenated audio stream
        from the compressed samples. Use when loading a sound tag
        for re-compression, re-sampling, or re-encoding.
        '''
        # default to regenerating to const.DEFAULT_UNCOMPRESSED_FORMAT
        # because, technically speaking, that is highest sample depth
        # we can ever possibly see in Halo CE.
        if compression is None: compression = const.DEFAULT_UNCOMPRESSED_FORMAT
        if sample_rate is None: sample_rate = self.sample_rate
        if encoding    is None: encoding    = self.encoding

        self._source_sample_data = self.get_concatenated_sample_data(
            compression, sample_rate, encoding
            )
        self._source_compression = compression
        self._source_sample_rate = sample_rate
        self._source_encoding    = encoding

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
                       export_source=True, decompress=True,
                       ext=const.CONTAINER_EXT_WAV, **kwargs):
        perm_chunks = []

        filepath = Path(util.BAD_PATH_CHAR_REMOVAL.sub("_", str(filepath_base)))
        filepath = Path("unnamed" if is_path_empty(filepath) else filepath)
        filepath = filepath.with_suffix(ext)
        
        if export_source and self.source_sample_data:
            # export the source data
            perm_chunks.append((
                filepath, self.compression, self.source_sample_rate, 
                self.source_encoding, self.source_sample_data,
                ))
        elif self.processed_samples:
            # concatenate processed samples if source samples don't exist.
            # if compression isn't some form of PCM, need to decompress it
            compression = self.compression
            if decompress or compression not in const.PCM_FORMATS:
                compression = const.COMPRESSION_PCM_16_LE

            try:
                sample_data = self.get_concatenated_sample_data(
                    compression, self.sample_rate, self.encoding
                    )
                if sample_data:
                    perm_chunks.append((
                        filepath, compression, self.sample_rate,
                        self.encoding, sample_data, 
                        ))
            except Exception:
                print("Could not decompress permutation pieces. Exporting in pieces.")
                # gotta switch format to the container it's compressed as
                for i, piece in enumerate(self.processed_samples):
                    ext = {
                        const.COMPRESSION_OGG:  const.CONTAINER_EXT_OGG,
                        const.COMPRESSION_OPUS: const.CONTAINER_EXT_OPUS,
                        const.COMPRESSION_FLAC: const.CONTAINER_EXT_FLAC,
                        }.get(piece.compression, ext)

                    name_base = "%s__%%s%s" % (filepath.stem, ext)
                    perm_chunks.append((
                        filepath.with_name(name_base % i), piece.compression, 
                        piece.sample_rate, piece.encoding, piece.sample_data
                        ))

        for perm_info in perm_chunks:
            filepath, comp, rate, enc, data = perm_info
            ext = filepath.suffix.lower()
            if not data or (not overwrite and filepath.is_file()):
                return
            elif ext not in const.SUPPORTED_EXPORT_EXTS:
                raise ValueError("Unsupported audio extension '%s'." % ext)
            elif ext in const.PYOGG_CONTAINER_EXTS:
                exporter = BlamSoundPermutation._export_to_pyogg_file
            else:
                exporter = BlamSoundPermutation._export_to_wav

            try:
                exporter(*perm_info, **kwargs)
            except Exception:
                print(format_exc())

    @staticmethod
    def _export_to_pyogg_file(
            filepath, compression, sample_rate, 
            encoding, sample_data, **kwargs
            ):
        ext = filepath.suffix.lower()
        if ext != const.CONTAINER_EXT_OGG:
            raise ValueError("Exporting '%s' is currently unsupported" % ext)
        elif compression != const.COMPRESSION_OGG:
            # need to encode data to oggvorbis first
            sample_data = ogg.encode_oggvorbis(
                sample_data, sample_rate,
                constants.sample_widths[compression], 
                constants.channel_counts[encoding], 
                util.is_big_endian_pcm(compression),
                **kwargs.get("ogg_kwargs", {})
                )

        filepath.parent.mkdir(exist_ok=True, parents=True)
        with filepath.open("wb") as f:
            f.write(sample_data)

    @staticmethod
    def _export_to_wav(
            filepath, compression, sample_rate, encoding, 
            sample_data, **kwargs
            ):
        if not (compression in const.PCM_FORMATS or 
                compression == const.COMPRESSION_IMA_ADPCM or
                compression == const.COMPRESSION_XBOX_ADPCM
                ):
            print("Unknown compression method:", compression)
            return

        block_ratio = 1
        block_size  = const.sample_widths[compression]
        if compression == const.COMPRESSION_IMA_ADPCM:
            # 16bit imaadpcm
            block_ratio /= const.IMA_ADPCM_DECOMPRESSED_BLOCKSIZE * 2
            block_size   = const.IMA_ADPCM_COMPRESSED_BLOCKSIZE
        elif compression == const.COMPRESSION_XBOX_ADPCM:
            # 16bit xbox adpcm
            block_ratio /= const.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE * 2
            block_size   = const.XBOX_ADPCM_COMPRESSED_BLOCKSIZE
        elif util.is_big_endian_pcm(compression):
            # one of the big-endian uncompressed pcm formats
            sample_data = util.convert_pcm_to_pcm(
                sample_data, compression,
                util.change_pcm_endianness(compression)
                )

        wav_file = wav_def.build()
        wav_file.filepath = filepath

        wav_fmt     = wav_file.data.wav_format
        wav_chunks  = wav_file.data.wav_chunks
        wav_chunks.append(case="data")
        data_chunk  = wav_chunks[-1]

        wav_fmt.channels        = const.channel_counts.get(encoding, 1)
        wav_fmt.sample_rate     = sample_rate
        wav_fmt.bits_per_sample = block_size * 8
        wav_fmt.block_align     = block_size * wav_fmt.channels
        wav_fmt.byte_rate       = int(
            sample_rate * wav_fmt.block_align * block_ratio
            )
        wav_fmt.fmt.data        = {
            const.COMPRESSION_IMA_ADPCM:  const.WAV_FORMAT_IMA_ADPCM,
            const.COMPRESSION_XBOX_ADPCM: const.WAV_FORMAT_XBOX_ADPCM,
            }.get(compression, const.WAV_FORMAT_PCM)

        data_chunk.data = sample_data
        wav_file.data.wav_header.filesize = 36 + len(sample_data)

        wav_file.serialize(temp=False, backup=False)

    def import_from_file(self, filepath):
        filepath = Path(filepath)
        if not filepath.is_file():
            raise OSError('File "%s" does not exist. Cannot import.' % filepath)

        ext = filepath.suffix.lower()
        if ext == const.CONTAINER_EXT_WAV:
            self._import_from_wav(filepath)
        elif (ext in const.PYOGG_CONTAINER_EXTS and
              ext in const.SUPPORTED_IMPORT_EXTS):
            self._import_from_pyogg_file(filepath, ext)
        else:
            raise ValueError("Unsupported audio extension '%s'." % ext)

        self._source_filename = filepath.name

    def _import_from_pyogg_file(self, filepath, ext):
        pyogg_audio_file = ogg.pyogg_audiofile_from_filepath(
            filepath, ext, streaming=False
            )
        sample_data = pyogg_audio_file.buffer
        sample_rate = pyogg_audio_file.frequency
        compression = const.OGG_DECOMPRESSED_FORMAT
        encoding    = (
            const.ENCODING_STEREO if pyogg_audio_file.channels == 2 else
            const.ENCODING_MONO   if pyogg_audio_file.channels == 1 else
            const.ENCODING_UNKNOWN
            )
        self.load_source_samples(sample_data, compression, sample_rate, encoding)

    def _import_from_wav(self, filepath):
        wav_file   = wav_def.build(filepath=filepath)
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
        elif wav_format.fmt.data not in const.ALLOWED_WAV_FORMATS:
            raise ValueError(
                'Invalid compression format "%s".' % wav_format.fmt.data)
        elif wav_format.channels not in (1, 2):
            raise ValueError(
                "Invalid number of channels. Must be 1 or 2, not %s." %
                wav_format.channels)
        elif wav_format.sample_rate == 0:
            raise ValueError(
                "Sample rate cannot be zero. Not a valid wav file")
        elif (wav_format.fmt.data == const.WAV_FORMAT_PCM_FLOAT and
              wav_format.bits_per_sample != 32):
            raise ValueError(
                "Pcm float sample width must be 32, not %s." %
                wav_format.bits_per_sample)
        elif (wav_format.fmt.data == const.WAV_FORMAT_PCM and
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
            encoding = const.ENCODING_STEREO
        else:
            encoding = const.ENCODING_MONO

        sample_data = data_chunk.data
        if wav_format.fmt.data == const.WAV_FORMAT_PCM_FLOAT:
            sample_data = util.convert_pcm_float32_to_pcm_int(sample_data, 4)
            compression = const.COMPRESSION_PCM_32_LE
        else:
            sample_width = None
            if wav_format.fmt.data == const.WAV_FORMAT_PCM:
                sample_width = wav_format.bits_per_sample // 8

            compression = const.wav_format_mapping.get(
                (wav_format.fmt.data, sample_width))

        self.load_source_samples(
            sample_data, compression, wav_format.sample_rate, encoding)
