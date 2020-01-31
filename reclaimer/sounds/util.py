#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import array
import audioop
import re
import struct
import sys

from reclaimer.sounds import constants

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


def get_sample_chunk_size(compression, encoding, chunk_size=None):
    if chunk_size is None:
        chunk_size = constants.MAX_SAMPLE_CHUNK_SIZE

    if compression == constants.COMPRESSION_XBOX_ADPCM:
        chunk_size = (
            chunk_size // constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE
            ) * constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE
    elif compression == constants.COMPRESSION_IMA_ADPCM:
        chunk_size = (
            chunk_size // constants.IMA_ADPCM_DECOMPRESSED_BLOCKSIZE
            ) * constants.IMA_ADPCM_COMPRESSED_BLOCKSIZE

    return chunk_size - (
        chunk_size % get_block_size(compression, encoding))


def get_block_size(compression, encoding):
    if compression == constants.COMPRESSION_OGG:
        return 1

    if compression == constants.COMPRESSION_XBOX_ADPCM:
        block_size = constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE
    elif compression == constants.COMPRESSION_IMA_ADPCM:
        block_size = constants.IMA_ADPCM_COMPRESSED_BLOCKSIZE
    else:
        block_size = constants.sample_widths[compression]
    return block_size * constants.channel_counts.get(encoding, 1)


def get_samples_per_block(compression):
    if compression == constants.COMPRESSION_XBOX_ADPCM:
        return constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2
    elif compression == constants.COMPRESSION_IMA_ADPCM:
        return constants.IMA_ADPCM_DECOMPRESSED_BLOCKSIZE // 2
    return 1


def get_sample_count(sample_data, compression, encoding):
    if compression == constants.COMPRESSION_OGG:
        raise NotImplementedError(
            "Cannot yet calculate ogg sample count")

    block_size = get_block_size(compression, encoding)
    chunk_count = len(sample_data) // block_size

    if compression == constants.COMPRESSION_XBOX_ADPCM:
        chunk_count *= constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2
    elif compression == constants.COMPRESSION_IMA_ADPCM:
        chunk_count *= constants.IMA_ADPCM_DECOMPRESSED_BLOCKSIZE // 2

    return chunk_count


def byteswap_pcm16_sample_data(samples):
    return convert_pcm_to_pcm(
        samples,
        constants.COMPRESSION_PCM_16_LE,
        constants.COMPRESSION_PCM_16_BE)


def is_big_endian_pcm(compression):
    '''
    Returns True if the endianness of the compression modes are different.
    Only considers the linear PCM formats.
    '''
    assert compression in constants.PCM_FORMATS
    if constants.sample_widths.get(compression, 1) == 1:
        return False

    return bool(compression & 1)


def change_pcm_endianness(compression):
    '''
    Returns the compression mode with endianness opposite
    that of the provided compression mode.
    Only considers the linear PCM formats.
    '''
    assert compression in constants.PCM_FORMATS
    if constants.sample_widths.get(compression, 1) == 1:
        return compression

    return compression ^ 1


def change_pcm_width(compression, new_width):
    '''
    Returns the compression mode at the specified width, but
    with the endianness of the provided compression mode.
    Only considers the linear PCM formats.
    '''
    assert compression in constants.PCM_FORMATS
    is_big_endian = is_big_endian_pcm(compression)

    if new_width == 4:
        new_compression = constants.COMPRESSION_PCM_32_LE
    elif new_width == 3:
        new_compression = constants.COMPRESSION_PCM_24_LE
    elif new_width == 2:
        new_compression = constants.COMPRESSION_PCM_16_LE
    elif new_width == 1:
        new_compression = constants.COMPRESSION_PCM_8_SIGNED
        is_big_endian = False

    return new_compression | int(is_big_endian)


def convert_pcm_to_pcm(samples, compression, target_compression,
                       encoding=constants.ENCODING_MONO,
                       target_encoding=constants.ENCODING_MONO,
                       sample_rate=constants.SAMPLE_RATE_22K,
                       target_sample_rate=constants.SAMPLE_RATE_22K):
    '''
    Converts a stream of PCM audio to one with a different compression
    and/or encoding and/or sample rate.
    '''
    assert compression in constants.PCM_FORMATS
    assert target_compression in constants.PCM_FORMATS
    current_width = constants.sample_widths.get(compression, 1)
    target_width  = constants.sample_widths.get(target_compression, 1)
    if len(samples) % current_width:
        # ensure samples are a multiple of their width
        samples = samples[: len(samples) - (len(samples) % current_width)]

    if compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift unsigned into signed
        samples = audioop.bias(samples, 1, 128)
    elif current_width > 1 and compression not in constants.NATIVE_ENDIANNESS_FORMATS:
        # byteswap samples to system endianness before processing
        samples = audioop.byteswap(samples, current_width)
        compression = change_pcm_endianness(compression)

    if current_width != target_width:
        samples = audioop.lin2lin(samples, current_width, target_width)

        # change compression to one with the correct sample width
        compression = change_pcm_width(compression, target_width)

    # make sure to convert to/from mono/stereo
    if encoding != target_encoding:
        if (encoding == constants.ENCODING_MONO and
            target_encoding == constants.ENCODING_STEREO):
            samples = audioop.tostereo(samples, target_width, 1, 1)
        elif (encoding == constants.ENCODING_STEREO and
              target_encoding == constants.ENCODING_MONO):
            samples = audioop.tomono(samples, target_width, 0.5, 0.5)
        else:
            raise ValueError("Can only convert between mono and stereo encodings.")
        encoding = target_encoding

    # convert sample rate if necessary
    if sample_rate != target_sample_rate:
        samples, _ = audioop.ratecv(
            samples, target_width, constants.channel_counts[encoding],
            sample_rate, target_sample_rate, None)
        sample_rate = target_sample_rate

    if target_compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift signed back into unsigned
        samples = audioop.bias(samples, 1, 128)
    elif target_width > 1 and (is_big_endian_pcm(compression) !=
                               is_big_endian_pcm(target_compression)):
        # byteswap samples to target endianness
        samples = audioop.byteswap(samples, target_width)

    return samples


def convert_pcm_float32_to_pcm_32(sample_data):
    samples = array.array('f', sample_data)
    if sys.byteorder == "big":
        samples.byteswap()

    samples = [-0x7fFFffFF if val <= -1.0 else
               (0x7fFFffFF if val >=  1.0 else
                int(val * 0x7fFFffFF))
               for val in samples]

    return struct.pack("<%di" % len(samples), *samples)


def generate_mouth_data(sample_data, compression, sample_rate, encoding):
    assert compression in constants.PCM_FORMATS
    assert encoding in constants.channel_counts
    assert sample_rate > 0

    sample_width = constants.sample_widths[compression]
    channel_count = constants.channel_counts[encoding]

    if compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift unsigned into signed
        sample_data = audioop.bias(sample_data, 1, 128)
    elif sample_width > 1 and compression not in constants.NATIVE_ENDIANNESS_FORMATS:
        # byteswap samples to system endianness before processing
        sample_data = audioop.byteswap(sample_data, sample_width)

    if sample_width == 2:
        sample_data = memoryview(sample_data).cast("h")
    elif sample_width == 4:
        sample_data = memoryview(sample_data).cast("i")

    # mouth data is sampled at 30Hz, so we divide the audio
    # sample_rate by that to determine how many samples we must
    # consider for each fragment. also, since mouth data doesn't
    # use multiple channels, and the audio samples are interleaved,
    # we multiply the channel count into the fragment_width.
    samples_per_mouth_sample = sample_rate / constants.SAMPLE_RATE_MOUTH_DATA
    fragment_width = int(
        channel_count * samples_per_mouth_sample + 0.5)

    # add fragment_width - 1 to round up to next multiple of fragment_width
    fragment_count = (
        len(sample_data) + fragment_width - 1) // fragment_width

    # used to scale the max fragment to the [0, 255] scale of a uint8
    scale_to_uint8 = 255 / ((1 << (sample_width * 8 - 1)) - 1)

    # generate mouth data samples
    mouth_data = bytearray(fragment_count)
    for i in range(fragment_count):
        fragment = sample_data[i * fragment_width:
                               (i + 1) * fragment_width]
        fragment_avg = sum(map(abs, fragment)) / samples_per_mouth_sample

        mouth_sample = fragment_avg * scale_to_uint8
        if mouth_sample >= 255:
            mouth_data[i] = 255
        else:
            mouth_data[i] = int(mouth_sample)

    # shift/scale the mouth samples based on the range of the mouth data
    mouth_avg = sum(mouth_data) / len(mouth_data)
    mouth_max = max(mouth_data)
    mouth_min = max(0, min(255, 2 * mouth_avg - mouth_max))

    mouth_range = (mouth_avg + mouth_max) / 2 - mouth_min
    if mouth_range == 0:
        # no range in the volume. don't try to scale
        # or shift, or else we'll divide by zero
        return bytes(mouth_data)

    for i in range(len(mouth_data)):
        mouth_sample = (mouth_data[i] - mouth_min) / mouth_range
        if mouth_sample >= 1.0:
            mouth_data[i] = 255
        elif mouth_sample <= 0.0:
            mouth_data[i] = 0
        else:
            mouth_data[i] = int(255 * mouth_sample)

    return bytes(mouth_data)
