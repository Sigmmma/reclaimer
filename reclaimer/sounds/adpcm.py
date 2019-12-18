import array
import audioop
import sys

from . import constants 

try:
    from .ext import adpcm_ext
    fast_adpcm = True
except:
    fast_adpcm = False

__all__ = (
    "decode_adpcm_samples",
    "encode_adpcm_samples",
    )


NOISE_SHAPING_OFF     = 0  # flat noise (no shaping)
NOISE_SHAPING_STATIC  = 1  # first-order highpass shaping
NOISE_SHAPING_DYNAMIC = 2  # dynamically tilted noise based on signal


def decode_adpcm_samples(in_data, channel_ct, output_big_endian=False):
    if channel_ct < 1:
        return b''
    elif not fast_adpcm:
        raise NotImplementedError(
            "Accelerator module not detected. Cannot decompress ADPCM.")

    # divide by 2 since we're treating out_data as a sint16 iterable
    out_data = array.array("h", (0,)) * (
        (len(in_data) // constants.XBOX_ADPCM_COMPRESSED_BLOCKSIZE) *
        (constants.XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE // 2))

    adpcm_ext.decode_xbadpcm_samples(in_data, out_data, channel_ct)

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
