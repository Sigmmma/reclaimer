from traceback import format_exc

from reclaimer.sounds import constants, ogg, util, adpcm


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
    @property
    def is_compressed(self):
        return self.compression not in constants.PCM_FORMATS

    def compress(self, target_compression, target_sample_rate=None,
                 target_encoding=None, vorbis_bitrate_info=None):
        if target_sample_rate is None:
            target_sample_rate = self.sample_rate

        if target_encoding is None:
            target_encoding = self.encoding

        if vorbis_bitrate_info is None:
            vorbis_bitrate_info = ogg.VorbisBitrateInfo()

        if self.is_compressed:
            raise ValueError("Cannot compress already compressed samples.")
        elif (target_compression == constants.COMPRESSION_OGG and
              not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError(
                "Ogg encoder not available. Cannot compress.")
        elif (target_compression not in constants.PCM_FORMATS and
              target_compression != constants.COMPRESSION_ADPCM and
              target_compression != constants.COMPRESSION_OGG):
              raise ValueError('Unknown compression type "%s"' %
                               target_compression)
        elif target_encoding not in (constants.ENCODING_MONO,
                                     constants.ENCODING_STEREO):
            raise ValueError("Compression encoding must be mono or stereo.")
        elif target_sample_rate <= 0:
            raise ValueError("Sample rate must be greater than zero.")

        sample_data = self.sample_data
        # make sure the sample data is the correct sample rate
        # and encoding before we try to compress it
        if (self.encoding != target_encoding or
            self.sample_rate != target_sample_rate):
            sample_data = util.convert_pcm_to_pcm(
                sample_data,
                self.compression, self.compression,
                self.encoding, target_encoding,
                self.sample_rate, target_sample_rate)

        if target_compression == constants.COMPRESSION_ADPCM:
            # compress to adpcm
            raise NotImplementedError("Whoops, adpcm is not implemented.")
        elif target_compression == constants.COMPRESSION_OGG:
            # compress to ogg vorbis
            raise NotImplementedError("Whoops, ogg is not implemented.")
        elif target_compression != self.compression:
            # convert to a different pcm format
            sample_data = util.convert_pcm_to_pcm(
                sample_data, self.compression, target_compression)

        self._sample_data = sample_data
        self._compression = target_compression
        self._encoding = target_encoding
        self._sample_rate = target_sample_rate

    def get_decompressed(self, target_compression, target_encoding=None):
        if target_encoding is None:
            target_encoding = self.encoding

        assert target_compression in constants.PCM_FORMATS
        assert target_encoding in constants.channel_counts

        curr_compression = self.compression
        if curr_compression == constants.COMPRESSION_ADPCM:
            # decompress adpcm to 16bit pcm
            sample_data = adpcm.decode_adpcm_samples(
                self.sample_data, constants.channel_counts.get(self.encoding, 1))
            curr_compression = constants.ADPCM_DECOMPRESSED_FORMAT
        elif not self.is_compressed:
            # samples are decompressed. use as-is
            sample_data = self.sample_data
        elif (curr_compression == constants.COMPRESSION_OGG and
              not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError(
                "Ogg decoder not available. Cannot decompress.")
        elif curr_compression == constants.COMPRESSION_WMA:
            raise NotImplementedError(
                "Wma decoder not available. Cannot decompress.")
        else:
            raise ValueError("Unknown compression format.")

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
