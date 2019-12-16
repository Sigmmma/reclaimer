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


def _slow_encode_adpcm_samples(in_data, out_data, channel_ct):
    pcm_blocksize   = channel_ct * XBOX_ADPCM_DECODED_BLOCKSIZE
    adpcm_blocksize = channel_ct * XBOX_ADPCM_ENCODED_BLOCKSIZE

    lin2adpcm = audioop.lin2adpcm

    state_packer = PyStruct("<hB").pack_into
    pcm_block_size = 2 * channel_ct
    
    all_states = [None] * channel_ct
    all_codes = [None] * channel_ct

    k = 0
    interleave = channel_ct > 1
    for i in range(0, len(in_data), pcm_blocksize):
        for c in range(channel_ct):
            # join all 4 bytes codes for this channel
            samples = b''.join(
                # join the 2 byte samples
                in_data[j: j + 2]
                for j in range(c * 2, pcm_blocksize, pcm_block_size)
                )
            all_codes[c], all_states[c] = lin2adpcm(samples, 2, all_states[c])
            state_packer(out_data, k, *all_states[c])
            k += 4

        # interleave the 32 byte code strings every 4 bytes
        codes = all_codes[c]
        if interleave:
            codes = b''.join(
                b''.join(codes[j: j + 4] for c in range(channel_ct))
                for j in range(0, 32, 4)
                )

        # swap the nibbles of the codes
        codes = bytes(map(NIBBLE_SWAP_MAPPING.__getitem__, codes))

        # write the 32 byte codes into the out_data
        out_data[k: k + len(codes)] = codes
        k += len(codes)


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

    if False and fast_adpcm:
        adpcm_ext.encode_adpcm_samples(in_data, out_data, channel_ct)
    else:
        _slow_encode_adpcm_samples(in_data, out_data, channel_ct)

    return bytes(out_data)
