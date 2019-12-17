import array
import audioop
import sys

from struct import Struct as PyStruct

try:
    from .ext import adpcm_ext
    fast_adpcm = True
except:
    fast_adpcm = False

__all__ = (
    "decode_adpcm_samples",
    "encode_adpcm_samples",
    )

NIBBLE_SWAP_MAPPING = tuple(((val&15)<<4) | (val>>4) for val in range(256))

# Byte size of an encoded xbox adpcm block
XBOX_ADPCM_ENCODED_BLOCKSIZE = 36
# Byte size of a decoded xbox adpcm block
XBOX_ADPCM_DECODED_BLOCKSIZE = 128


NOISE_SHAPING_OFF     = 0  # flat noise (no shaping)
NOISE_SHAPING_STATIC  = 1  # first-order highpass shaping
NOISE_SHAPING_DYNAMIC = 2  # dynamically tilted noise based on signal


def _slow_decode_adpcm_samples(in_data, out_data, channel_ct):
    # divide by 2 since we're treating out_data as a sint16 iterable
    pcm_blocksize   = channel_ct * XBOX_ADPCM_DECODED_BLOCKSIZE // 2
    adpcm_blocksize = channel_ct * XBOX_ADPCM_ENCODED_BLOCKSIZE

    adpcm2lin = audioop.adpcm2lin
    all_codes = memoryview(in_data)

    state_unpacker = PyStruct("<" + "hBx" * channel_ct).unpack_from
    code_block_size = 4 * channel_ct

    k = 0
    interleaved = channel_ct > 1
    for i in range(0, len(in_data), adpcm_blocksize):
        state_vals = state_unpacker(in_data, i)
        all_states = tuple(zip(state_vals[::2], state_vals[1::2]))
        all_swapped_codes = bytes(map(
            NIBBLE_SWAP_MAPPING.__getitem__,
            all_codes[i + code_block_size: i + adpcm_blocksize]))

        for c in range(channel_ct):
            # join all 4 bytes codes for this channel
            swapped_codes = all_swapped_codes
            if interleaved:
                swapped_codes = b''.join(
                    # join the 4 byte codes
                    swapped_codes[j: j + 4]
                    for j in range(c * 4, len(swapped_codes), code_block_size)
                    )
            decoded_samples = memoryview(
                adpcm2lin(swapped_codes, 2, all_states[c])[0]).cast("h")

            # interleave the samples for each channel
            out_data[k + c: k + pcm_blocksize: channel_ct] = array.array(
                "h", decoded_samples)

        k += pcm_blocksize


def decode_adpcm_samples(in_data, channel_ct, output_big_endian=False):
    if channel_ct < 1:
        return b''

    # divide by 2 since we're treating out_data as a sint16 iterable
    out_data = array.array("h", (0,)) * (
        (len(in_data) // XBOX_ADPCM_ENCODED_BLOCKSIZE) *
        (XBOX_ADPCM_DECODED_BLOCKSIZE // 2))

    if fast_adpcm:
        adpcm_ext.decode_adpcm_samples(in_data, out_data, channel_ct)
    else:
        _slow_decode_adpcm_samples(in_data, out_data, channel_ct)

    if (sys.byteorder == "big") != output_big_endian:
        out_data.byteswap()

    return bytes(out_data)


def encode_adpcm_samples(in_data, channel_ct, input_big_endian=False):
    if channel_ct < 1:
        return b''

    if (sys.byteorder == "big") != input_big_endian:
        out_data = audioop.byteswap(out_data, 2)

    pad_size = (len(in_data) // channel_ct) % XBOX_ADPCM_DECODED_BLOCKSIZE
    if pad_size:
        # repeat the last sample to the end to pad to a multiple of blocksize
        in_data += in_data[-(channel_ct * 2): ] * pad_size

    out_data = bytearray(
        (len(in_data) // XBOX_ADPCM_DECODED_BLOCKSIZE) *
        XBOX_ADPCM_ENCODED_BLOCKSIZE
        )

    if not fast_adpcm:
        raise NotImplementedError(
            "Accelerator module not detected. Cannot compress to ADPCM.")

    adpcm_ext.encode_adpcm_samples(in_data, out_data, channel_ct)

    return bytes(out_data)
