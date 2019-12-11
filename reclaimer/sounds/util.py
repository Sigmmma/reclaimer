import array
import audioop
import re

from reclaimer.sounds import constants

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


def get_sample_chunk_size(compression, encoding,
                          max_chunk_size=constants.MAX_SAMPLE_CHUNK_SIZE):
    if compression == constants.COMPRESSION_OGG:
        return constants.MAX_OGG_DECOMP_BUFFER_SIZE

    if compression == constants.COMPRESSION_ADPCM:
        chunk_size = constants.ADPCM_SAMPLE_CHUNK_SIZE
    else:
        chunk_size = max_chunk_size

    chunk_size = min(chunk_size, constants.MAX_SAMPLE_CHUNK_SIZE)

    return chunk_size - (
        chunk_size % get_block_size(compression, encoding))


def get_block_size(compression, encoding):
    if compression == constants.COMPRESSION_OGG:
        return 1

    if compression == constants.COMPRESSION_ADPCM:
        block_size = constants.ADPCM_COMPRESSED_BLOCKSIZE
    else:
        block_size = constants.sample_widths[compression]
    return block_size * constants.channel_counts.get(encoding, 1)


def get_samples_per_block(compression):
    if compression == constants.COMPRESSION_ADPCM:
        return constants.ADPCM_DECOMPRESSED_BLOCKSIZE // 2
    return 1


def get_sample_count(sample_data, compression, encoding):
    if compression == constants.COMPRESSION_OGG:
        raise NotImplementedError(
            "Cannot yet calculate ogg sample count")

    block_size = get_block_size(compression, encoding)
    chunk_count = len(sample_data) // block_size

    if compression == constants.COMPRESSION_ADPCM:
        chunk_count *= constants.ADPCM_DECOMPRESSED_BLOCKSIZE // 2

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
        new_compression = COMPRESSION_PCM_8_SIGNED
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


def generate_mouth_data(sample_data, compression, sample_rate, encoding):
    assert compression in constants.PCM_FORMATS
    assert encoding in constants.channel_counts
    assert sample_rate > 0

    # TODO: Finish making this function generate data
    #       identical to that which tool.exe outputs.

    sample_width = constants.sample_widths[compression]
    channel_count = constants.channel_counts[encoding]

    if compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift unsigned into signed
        sample_data = audioop.bias(sample_data, 1, 128)
    elif sample_width > 1 and compression not in constants.NATIVE_ENDIANNESS_FORMATS:
        # byteswap samples to system endianness before processing
        sample_data = audioop.byteswap(sample_data, sample_width)

    if sample_rate > constants.SAMPLE_RATE_VOICE:
        sample_data = convert_pcm_to_pcm(
            sample_data, compression, compression, encoding, encoding,
            sample_rate, constants.SAMPLE_RATE_VOICE
            )
        sample_rate = constants.SAMPLE_RATE_VOICE

    # make this a memoryview to make it more efficient(copies of slices
    # won't be created each time we pass a slice to audioop.max)
    slicable_samples = memoryview(sample_data)

    # fragment_width will be number of bytes for all the samples
    # that must be scanned to calculate one mouth data sample.

    # mouth data is sampled at 30Hz, so we divide the audio
    # sample_rate by that to determine how many samples we must
    # consider for each fragment. also, since mouth data doesn't
    # use multiple channels, and the audio samples are interleaved,
    # we multiply the channel count into the fragment_width.
    fragment_width = int(
        sample_width * channel_count *
        (sample_rate / constants.SAMPLE_RATE_MOUTH_DATA) + 0.5)

    # add fragment_width - 1 to round up to next multiple of fragment_width
    fragment_count = (
        len(sample_data) + fragment_width - 1) // fragment_width

    # used to scale the max fragment to the [0, 255] scale of a uint8
    max_scale = 1 / (1 << (8 * sample_width - 1))
    power_scale = max_scale * 2
    j = 0
    # generate mouth data samples
    mouth_data = bytearray(fragment_count)
    for i in range(0, fragment_count * fragment_width, fragment_width):
        fragment = slicable_samples[i: i + fragment_width]
        fragment_max = audioop.max(fragment, sample_width) * max_scale
        fragment_power = audioop.rms(fragment, sample_width) * power_scale
        mouth_sample = fragment_max * fragment_power
        if mouth_sample > 1.0:
            mouth_sample = 1.0

        mouth_sample = audioop.max(fragment, sample_width) * max_scale
        mouth_data[j] = int(mouth_sample * 255.5)
        j += 1

    return bytes(mouth_data)
