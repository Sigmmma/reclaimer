import array
import audioop

from reclaimer.sounds import constants


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


def downsample_half(samples, compression):
    '''Used to downsample to half sample rate(44100 to 22050)'''
    assert compression in constants.PCM_FORMATS
    width = constants.sample_widths.get(compression, 1)

    if width == 4:
        samples = array.array("i", samples)
    elif width == 4:
        samples = array.array("h", samples)
    elif compression == constants.COMPRESSION_PCM_8_SIGNED:
        samples = array.array("b", samples)
    elif compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift unsigned into signed
        samples = array.array("B", audioop.bias(samples, 1, 128))

    samples = array.array(
        samples.typecode,
        ((samples[i] + samples[i + 1]) // 2
         for i in range(0, len(samples), 2))
        ).tobytes()
    

    if compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 128 to shift signed back into signed
        samples = audioop.bias(samples, 1, 127)

    return samples


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


def convert_pcm_to_pcm(samples, compression, target_compression):
    '''
    Converts a stream of PCM audio in one compression to another compression.
    '''
    current_width = constants.sample_widths.get(curr_compression, 1)
    target_width  = constants.sample_widths.get(target_compression, 1)
    if len(samples) % current_width:
        # ensure samples are a multiple of their width
        samples = samples[: len(samples) - (len(samples) % current_width)]


    if current_width != target_width:
        # sample width needs to be adjusted to target
        if compression == constants.COMPRESSION_PCM_8_UNSIGNED:
            # bias by 128 to shift unsigned into signed
            samples = audioop.bias(samples, 1, 128)
        elif current_width > 1 and compression not in constants.NATIVE_ENDIANNESS_FORMATS:
            # byteswap samples to system endianness before adjusting width
            samples = audioop.byteswap(samples, current_width)
            compression = change_pcm_endianness(compression)

        samples = audioop.lin2lin(samples, current_width, target_width)

        # change compression to one with the correct sample width
        compression = change_pcm_width(compression, target_width)


    if target_compression == constants.COMPRESSION_PCM_8_UNSIGNED:
        # bias by 127 to shift signed back into unsigned
        samples = audioop.bias(samples, 1, 127)
    elif target_width > 1 and (is_big_endian_pcm(compression) !=
                               is_big_endian_pcm(target_compression)):
        # byteswap samples to target endianness
        samples = audioop.byteswap(samples, target_width)

    return samples
