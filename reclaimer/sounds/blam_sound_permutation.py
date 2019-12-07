import audioop
import os

from array import array
from traceback import format_exc

from reclaimer.sounds import constants
from reclaimer.sounds import util
from reclaimer.sounds.adpcm import decode_adpcm_samples

from supyr_struct.defs.audio.wav import wav_def


class BlamSoundSamples:
    _sample_data = b''
    _sample_count = 0
    _compression = constants.COMPRESSION_PCM_16_LE
    _sample_rate = constants.SAMPLE_RATE_22K
    _encoding = constants.ENCODING_MONO
    _mouth_data = b''
    def __init__(self, sample_data, sample_count, compression,
                 sample_rate, encoding, mouth_data=b''):
        self._sample_data = sample_data
        self._sample_count = sample_count
        self._compression = compression
        self._sample_rate = sample_rate
        self._encoding = encoding
        self._mouth_data = mouth_data

    @property
    def sample_data(self):
        return self._sample_data
    @property
    def mouth_data(self):
        return self._mouth_data
    @property
    def sample_count(self):
        return self._sample_count
    @property
    def compression(self):
        return self._compression
    @property
    def sample_rate(self):
        return self._sample_rate
    @property
    def encoding(self):
        return self._encoding

    def compress(self, target_compression, target_encoding=None):
        pass

    def get_decompressed(self, target_compression, target_encoding=None):
        if target_encoding is None:
            target_encoding = self.encoding

        assert target_compression in constants.PCM_FORMATS
        assert target_encoding in constants.channel_counts

        if self.compression == constants.COMPRESSION_ADPCM:
            # decompress adpcm to 16bit pcm
            sample_data = decode_adpcm_samples(
                self.sample_data, constants.channel_counts.get(self.encoding, 1))
            curr_compression = constants.ADPCM_DECOMPRESSED_FORMAT
        elif self.compression in constants.PCM_FORMATS:
            # samples are decompressed. use as-is
            sample_data = self.sample_data
            curr_compression = self.compression
        elif (self.compression == constants.COMPRESSION_OGG and
              not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError("Ogg encoder not available. Cannot compress.")
        else:
            raise NotImplementedError("whoops, decompressing this isn't implemented.")

        if (curr_compression != target_compression or
            self.encoding != target_encoding):
            sample_data = util.convert_pcm_to_pcm(
                sample_data, curr_compression, target_compression,
                self.encoding, target_encoding)

        return sample_data

    def generate_mouth_data(self):
        # decompress to constants.ADPCM_DECOMPRESSED_FORMAT
        # as it is guaranteed to be a decompressed PCM format,
        # is guaranteed to be the correct system endianness,
        # and is high enough fidelity to generate mouth_data.
        sample_data = self.get_decompressed(
            constants.ADPCM_DECOMPRESSED_FORMAT, self.encoding)

        self._mouth_data = util.generate_mouth_data(
            sample_data, constants.ADPCM_DECOMPRESSED_FORMAT,
            self.sample_rate, self.encoding)


class BlamSoundPermutation:
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

    def partition_samples(self, compression, sample_rate=None, chunk_size=0):
        if (compression == constants.COMPRESSION_OGG and
            not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError(
                "Ogg encoder not available. Cannot partition.")

        if sample_rate is None:
            sample_rate = self.source_sample_rate

        chunk_size = util.calculate_sample_chunk_size(
            compression, chunk_size, encoding)

        sample_data = self.source_sample_data
        if sample_rate != self.source_sample_rate:
            # resample to the target sample rate
            audioop.ratecv(
                sample_data,
                constants.sample_widths[self.source_encoding],
                constants.channel_counts[self.source_encoding],
                self.source_sample_rate, sample_rate, None)

        # TODO: Finish this

    def generate_mouth_data(self):
        for samples in self.processed_samples:
            samples.generate_mouth_data()

    def compress_samples(self, compression, sample_rate=None):
        if sample_rate is None:
            sample_rate = self.source_sample_rate

        if (compression == constants.COMPRESSION_OGG and
            not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError(
                "Ogg encoder not available. Cannot compress.")

        for samples in self.processed_samples:
            samples.compress(compression)

    def get_concatenated_sample_data(self, target_compression=None,
                                     target_encoding=None):
        if target_compression is None:
            target_compression = self.source_compression
        if target_encoding is None:
            target_encoding = self.source_encoding

        assert target_encoding in constants.channel_counts

        if target_compression != self.compression or target_encoding != self.encoding:
            # decompress processed samples to the target compression
            sample_data = b''.join(
                p.get_decompressed(target_compression, target_encoding)
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
            constants.DEFAULT_UNCOMPRESSED_FORMAT, self.encoding)
        self._source_compression = constants.DEFAULT_UNCOMPRESSED_FORMAT
        self._source_sample_rate = self.sample_rate
        self._source_encoding = self.encoding

    @classmethod
    def create_from_file(filepath):
        try:
            new_perm = BlamSoundPermutation()
            new_perm.import_from_file(filepath)
        except Exception:
            print(format_exc())

        if not new_perm.source_sample_data:
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
                (compression, self.source_encoding, self.source_sample_data)
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
                    compression, encoding)
                if sample_data:
                    perm_chunks.append((compression, self.encoding, sample_data))
            except Exception:
                perm_chunks.extend(
                    (piece.compression, piece.encoding, piece.sample_data)
                    for piece in self.processed_samples
                    )

        i = -1
        wav_file = wav_def.build()
        for compression, encoding, sample_data in perm_chunks:
            i += 1
            filepath = util.BAD_PATH_CHAR_REMOVAL.sub("_", filepath_base)

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

            if not sample_data or (not overwrite and os.path.isfile(filepath)):
                continue

            if is_container_format:
                try:
                    folderpath = os.path.dirname(filepath)
                    # If the path doesnt exist, create it
                    if not os.path.exists(folderpath):
                        os.makedirs(folderpath)

                    with open(filepath, "wb") as f:
                        f.write(sample_data)
                except Exception:
                    print(format_exc())

                continue

            wav_file.filepath = filepath

            wav_fmt = wav_file.data.format
            wav_fmt.fmt.set_to('pcm')
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
            elif compression == constants.COMPRESSION_ADPCM:
                # 16bit adpcm
                wav_fmt.fmt.set_to('ima_adpcm')
                wav_fmt.bits_per_sample = 16
                wav_fmt.block_align = constants.ADPCM_COMPRESSED_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(
                    (wav_fmt.sample_rate * wav_fmt.block_align /
                     (constants.ADPCM_DECOMPRESSED_BLOCKSIZE // 2))
                    )
            else:
                print("Unknown compression method:", compression)
                continue

            wav_file.data.wav_data.audio_data = sample_data
            wav_file.data.wav_data.audio_data_size = samples_len
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)

    def import_from_file(self, filepath):
        # TODO: Make this accept loading wav and possibly ogg files.
        pass
