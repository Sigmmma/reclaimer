#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

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
                 target_encoding=None, **compressor_kwargs):
        if target_sample_rate is None:
            target_sample_rate = self.sample_rate

        if target_encoding is None:
            target_encoding = self.encoding

        if (target_compression == self.compression and
            target_sample_rate == self.sample_rate and
            target_encoding == self.encoding):
            # compressing to same settings. nothing to do.
            return

        if (target_compression == constants.COMPRESSION_OGG and
              not constants.OGG_VORBIS_AVAILABLE):
            raise NotImplementedError(
                "Ogg encoder not available. Cannot compress.")
        elif (target_compression not in constants.PCM_FORMATS and
              target_compression != constants.COMPRESSION_XBOX_ADPCM and
              target_compression != constants.COMPRESSION_IMA_ADPCM and
              target_compression != constants.COMPRESSION_OGG):
            raise ValueError('Unknown compression type "%s"' %
                             target_compression)
        elif target_encoding not in (constants.ENCODING_MONO,
                                     constants.ENCODING_STEREO):
            raise ValueError("Compression encoding must be mono or stereo.")
        elif target_sample_rate <= 0:
            raise ValueError("Sample rate must be greater than zero.")

        sample_data = self.sample_data
        compression = self.compression
        if self.is_compressed:
            # decompress samples so we can recompress(ugh, whatever, i don't care)
            compression = (
                constants.ADPCM_DECOMPRESSED_FORMAT if
                compression in (constants.COMPRESSION_XBOX_ADPCM,
                                constants.COMPRESSION_IMA_ADPCM)
                else constants.HIGHEST_FIDELITY_FORMAT)
            sample_data = self.get_decompressed(
                compression, self.sample_rate, self.encoding)

        # make sure the sample data is the correct sample rate
        # and encoding before we try to compress it
        if (self.encoding != target_encoding or
            self.sample_rate != target_sample_rate):
            sample_data = util.convert_pcm_to_pcm(
                sample_data,
                self.compression, self.compression,
                self.encoding, target_encoding,
                self.sample_rate, target_sample_rate)

        if target_compression in (constants.COMPRESSION_XBOX_ADPCM,
                                  constants.COMPRESSION_IMA_ADPCM):
            # compress to adpcm
            if constants.sample_widths[compression] != 2:
                # adpcm encoder only accepts 16bit pcm as input
                sample_data = util.convert_pcm_to_pcm(
                    sample_data, compression,
                    constants.ADPCM_DECOMPRESSED_FORMAT)
                compression = constants.ADPCM_DECOMPRESSED_FORMAT

            adpcm_kwargs = compressor_kwargs.get("adpcm_kwargs", {})

            sample_data = adpcm.encode_adpcm_samples(
                sample_data, constants.channel_counts[target_encoding],
                util.is_big_endian_pcm(compression), **adpcm_kwargs)
        elif target_compression == constants.COMPRESSION_OGG:
            # compress to ogg vorbis
            # TODO: Finish this
            ogg_kwargs = compressor_kwargs.get("ogg_kwargs", {})

            raise NotImplementedError("Whoops, ogg is not implemented.")
        elif target_compression != self.compression:
            # convert to a different pcm format
            sample_data = util.convert_pcm_to_pcm(
                sample_data, self.compression, target_compression)

        self._sample_data = sample_data
        self._compression = target_compression
        self._encoding = target_encoding
        self._sample_rate = target_sample_rate

    def get_decompressed(self, target_compression, target_sample_rate=None,
                         target_encoding=None):
        if target_encoding is None:
            target_encoding = self.encoding

        if target_sample_rate is None:
            target_sample_rate = self.sample_rate

        assert target_compression in constants.PCM_FORMATS
        assert target_encoding in constants.channel_counts
        assert target_sample_rate > 0

        curr_compression = self.compression
        if curr_compression in (constants.COMPRESSION_XBOX_ADPCM,
                                constants.COMPRESSION_IMA_ADPCM):
            # decompress adpcm to 16bit pcm
            sample_data = adpcm.decode_adpcm_samples(
                self.sample_data, constants.channel_counts[self.encoding],
                util.is_big_endian_pcm(target_compression))
            curr_compression = constants.ADPCM_DECOMPRESSED_FORMAT
        elif not self.is_compressed:
            # samples are decompressed. use as-is
            sample_data = self.sample_data
        elif curr_compression == constants.COMPRESSION_OGG:
            if not constants.OGG_VORBIS_AVAILABLE:
                raise NotImplementedError(
                    "Ogg decoder not available. Cannot decompress.")
            # TODO: Finish this
        elif curr_compression == constants.COMPRESSION_WMA:
            if not constants.WMA_AVAILABLE:
                raise NotImplementedError(
                    "Wma decoder not available. Cannot decompress.")
            # TODO: Finish this
        else:
            raise ValueError("Unknown compression format.")

        if (curr_compression != target_compression or
            self.encoding != target_encoding or
            self.sample_rate != target_sample_rate):
            sample_data = util.convert_pcm_to_pcm(
                sample_data, curr_compression, target_compression,
                self.encoding, target_encoding,
                self.sample_rate, target_sample_rate)

        return sample_data

    def generate_mouth_data(self):
        # decompress to constants.DEFAULT_UNCOMPRESSED_FORMAT
        # as it is guaranteed to be a decompressed PCM format,
        # is guaranteed to be the correct system endianness,
        # and is high enough fidelity to generate mouth_data.
        sample_data = self.get_decompressed(
            constants.DEFAULT_UNCOMPRESSED_FORMAT,
            self.sample_rate, self.encoding)

        self._mouth_data = util.generate_mouth_data(
            sample_data, constants.DEFAULT_UNCOMPRESSED_FORMAT,
            self.sample_rate, self.encoding)
