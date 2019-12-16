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
    "decode_adpcm_samples", "get_adpcm_blocksize", "get_pcm_blocksize",
    )

NIBBLE_SWAP_MAPPING = tuple(((val&15)<<4) | (val>>4) for val in range(256))

# Byte size of an encoded xbox adpcm block
XBOX_ADPCM_ENCODED_BLOCKSIZE = 36
# Byte size of a decoded xbox adpcm block
XBOX_ADPCM_DECODED_BLOCKSIZE = 128


def slow_decode_adpcm_samples(in_data, channel_ct):
    if channel_ct < 1:
        return b''

    adpcm2lin = audioop.adpcm2lin
    encoded_blocksize = channel_ct * XBOX_ADPCM_ENCODED_BLOCKSIZE
    decoded_blocksize = channel_ct * XBOX_ADPCM_DECODED_BLOCKSIZE
    # divide by 2 since we're treating out_data as a sint16 iterable
    decoded_blocksize = decoded_blocksize // 2

    block_ct = len(in_data) // encoded_blocksize
    out_data = array.array("h", (0,)) * (block_ct * decoded_blocksize)
    codes = memoryview(in_data)

    state_unpacker = PyStruct("<" + "hBx" * channel_ct).unpack_from
    block_size = 4 * channel_ct

    k = 0
    for i in range(0, len(in_data), encoded_blocksize):
        state_vals = state_unpacker(in_data, i)
        states = tuple(zip(state_vals[::2], state_vals[1::2]))
        all_swapped_codes = bytes(map(
            NIBBLE_SWAP_MAPPING.__getitem__,
            codes[i + block_size: i + encoded_blocksize]))

        for c in range(channel_ct):
            # join all 4 bytes codes for this channel
            swapped_codes = b''.join(
                # join the 4 byte codes
                all_swapped_codes[j: j + 4]
                for j in range(c * 4, len(all_swapped_codes), block_size)
                )
            decoded_samples = memoryview(
                adpcm2lin(swapped_codes, 2, states[c])[0]).cast("h")

            # interleave the samples for each channel
            out_data[k + c: k + decoded_blocksize: channel_ct] = array.array(
                "h", decoded_samples)

        k += decoded_blocksize

    return out_data


def decode_adpcm_samples(in_data, channel_ct):
    if fast_adpcm:
        block_ct = len(in_data) // (channel_ct * XBOX_ADPCM_ENCODED_BLOCKSIZE)
        out_data = array.array("h", (0,)) * (
            block_ct * channel_ct * XBOX_ADPCM_DECODED_BLOCKSIZE // 2)

        adpcm_ext.decode_adpcm_samples(in_data, out_data, channel_ct)
    else:
        out_data = slow_decode_adpcm_samples(in_data, channel_ct)

    if sys.byteorder == "big":
        # always return as little endian
        out_data.byteswap()

    return bytes(out_data)
