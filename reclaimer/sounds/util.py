import array
import audioop
import re

from reclaimer.sounds import constants

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


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
        new_compression = COMPRESSION_PCM_8_SIGNED
        is_big_endian = False

    return new_compression | int(is_big_endian)


def convert_pcm_to_pcm(samples, compression, target_compression,
                       encoding=constants.ENCODING_MONO,
                       target_encoding=constants.ENCODING_MONO):
    '''
    Converts a stream of PCM audio in one compression to another compression.
    '''
    current_width = constants.sample_widths.get(curr_compression, 1)
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

    if target_compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift signed back into unsigned
        samples = audioop.bias(samples, 1, 128)
    elif target_width > 1 and (is_big_endian_pcm(compression) !=
                               is_big_endian_pcm(target_compression)):
        # byteswap samples to target endianness
        samples = audioop.byteswap(samples, target_width)

    return samples


def generate_mouth_data(sample_data, compression, sample_rate, encoding):
    assert compression in constants.PCM_FORMATS
    assert encoding in constants.channel_counts
    assert sample_rate > 0

    sample_width = constants.sample_widths[compression]

    if compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift unsigned into signed
        sample_data = audioop.bias(sample_data, 1, 128)
    elif sample_width > 1 and compression not in constants.NATIVE_ENDIANNESS_FORMATS:
        # byteswap samples to system endianness before processing
        sample_data = audioop.byteswap(sample_data, sample_width)

    # fragment_width will be number of bytes for all the samples
    # that must be scanned to calculate one mouth data sample.

    # mouth data is sampled at 30Hz, so we divide the audio
    # sample_rate by that to determine how many samples we must
    # consider for each fragment. also, since mouth data doesn't
    # use multiple channels, and the audio samples are interleaved,
    # we multiply the channel count into the fragment_width.
    fragment_width = int(
        sample_width * constants.channel_counts[encoding] *
        (sample_rate / constants.MOUTH_DATA_SAMPLE_RATE) + 0.5)

    # add fragment_width - 1 to round up to next multiple of fragment_width
    fragment_count = (
        len(sample_data) + fragment_width - 1) // fragment_width

    # generate mouth data samples
    mouth_data = bytearray(fragment_count)
    # make this a memoryview to make it more efficient(copies of slices
    # won't be created each time we pass a slice to get_fragment_max)
    slicable_samples = memoryview(sample_data)
    # used to scale the max fragment to the [0, 255] scale of a uint8
    sample_scale = 255.5 / ((1 << (8 * sample_width - 1)) - 1)
    j = 0
    for i in range(0, fragment_count * fragment_width, fragment_width):
        fragment_max = audioop.max(
            slicable_samples[i: i + fragment_width], sample_width)
        mouth_data[j] = int(sample_scale * fragment_max)
        j += 1

    return bytes(mouth_data)
