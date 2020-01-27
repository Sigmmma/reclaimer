# ISC License (ISC)
#
# Copyright 2017 Devin Bobadilla
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
# IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import array
import audioop
import sys

from struct import unpack_from
from types import MethodType

from . import constants

try:
    from .ext import adpcm_ext
    fast_adpcm = True
except:
    fast_adpcm = False

__all__ = (
    "decode_adpcm_samples",
    "encode_adpcm_samples",
    "NOISE_SHAPING_OFF", "NOISE_SHAPING_STATIC", "NOISE_SHAPING_DYNAMIC",
    )

NIBBLE_SWAP_MAPPING = tuple(((val&15)<<4) | (val>>4) for val in range(256))


NOISE_SHAPING_OFF     = 0  # flat noise (no shaping)
NOISE_SHAPING_STATIC  = 1  # first-order highpass shaping
NOISE_SHAPING_DYNAMIC = 2  # dynamically tilted noise based on signal


def _slow_decode_xbadpcm_samples(in_data, out_data, channel_ct):
    # divide by 2 since we're treating out_data as a sint16 iterable
    pcm_blocksize   = channel_ct * constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2
    adpcm_blocksize = channel_ct * constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE

    adpcm2lin = audioop.adpcm2lin
    all_codes = memoryview(in_data)

    state_unpacker = MethodType(unpack_from, "<" + "hBx" * channel_ct)
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
            out_data[k + c] = all_states[c][0]
            out_data[k + c + channel_ct: k + pcm_blocksize: channel_ct] = array.array(
                "h", decoded_samples)[: -1]

        k += pcm_blocksize


def decode_adpcm_samples(in_data, channel_ct, output_big_endian=False):
    if channel_ct < 1:
        return b''

    # divide by 2 since we're treating out_data as a sint16 iterable
    out_data = array.array("h", (0,)) * (
        (len(in_data) // constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE) *
        (constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2))

    if fast_adpcm:
        adpcm_ext.decode_xbadpcm_samples(in_data, out_data, channel_ct)
    else:
        _slow_decode_xbadpcm_samples(in_data, out_data, channel_ct)

    if (sys.byteorder == "big") != output_big_endian:
        out_data.byteswap()

    return bytes(out_data)


def encode_adpcm_samples(in_data, channel_ct, input_big_endian=False,
                         noise_shaping=NOISE_SHAPING_OFF, lookahead=3):
    assert noise_shaping in (NOISE_SHAPING_OFF, NOISE_SHAPING_STATIC, NOISE_SHAPING_DYNAMIC)
    assert lookahead in range(6)

    if channel_ct < 1:
        return b''
    elif not fast_adpcm:
        raise NotImplementedError(
            "Accelerator module not detected. Cannot compress to ADPCM.")

    if (sys.byteorder == "big") != input_big_endian:
        out_data = audioop.byteswap(out_data, 2)

    adpcm_blocksize = constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE * channel_ct
    pcm_blocksize = constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE * channel_ct

    pad_size = len(in_data) % pcm_blocksize
    if pad_size:
        pad_size = pcm_blocksize - pad_size
        # repeat the last sample to the end to pad to a multiple of blocksize
        pad_piece_size = (channel_ct * 2)
        in_data += in_data[-pad_piece_size: ] * (pad_size // pad_piece_size)

    out_data = bytearray(
        (len(in_data) // pcm_blocksize) * adpcm_blocksize
        )

    adpcm_ext.encode_xbadpcm_samples(
        in_data, out_data, channel_ct, noise_shaping, lookahead)

    return bytes(out_data)
