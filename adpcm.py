import audioop
from array import array
from struct import Struct

__all__ = ("decode_adpcm_samples", "ADPCM_BLOCKSIZE", "PCM_BLOCKSIZE", )

STEP_TABLE = (
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
    )
INDEX_TABLE = (
    -1, -1, -1, -1, 2, 4, 6, 8,
    -1, -1, -1, -1, 2, 4, 6, 8
    )

ADPCM_BLOCKSIZE = 36
PCM_BLOCKSIZE   = 130


def _fast_decode_mono_adpcm_samples(samples, endian="<"):
    adpcm2lin = audioop.adpcm2lin

    pcm_size   = PCM_BLOCKSIZE
    adpcm_size = ADPCM_BLOCKSIZE
    state_size = 4

    block_ct = len(samples) // adpcm_size
    out_data = bytearray(block_ct * pcm_size)

    pcm_i = 0
    unpacker = Struct(endian + "hh").unpack_from
    for i in range(0, len(samples), adpcm_size):
        # why couldn't it be nice and just follow the same
        # step packing pattern where the first step is the
        # first 4 bits and the second is the last 4 bits.
        steps = bytes(((b<<4) + (b>>4))&0xFF for b in
                      samples[i + state_size: i + adpcm_size])
        predictor = samples[i: i+2]
        if endian == ">":
            predictor = predictor[::-1]

        out_data[pcm_i: pcm_i + pcm_size] = (
            predictor + adpcm2lin(steps, 2, unpacker(samples, i))[0]
            )

        pcm_i += pcm_size

    return array("h", out_data)


def decode_adpcm_samples(samples, channel_ct, endian="<"):
    if channel_ct <= 0:
        return
    elif channel_ct == 1:
        return _fast_decode_mono_adpcm_samples(samples, endian)

    pcm_mask  = 1 << 16
    code_shifts = tuple(range(0, 8*4, 4))
    step_table  = STEP_TABLE
    index_table = INDEX_TABLE
    adpcm_size  = channel_ct * ADPCM_BLOCKSIZE // 2
    skip_size   = channel_ct * 2
    code_skip_size = skip_size * 8

    block_ct = len(samples) // (channel_ct * ADPCM_BLOCKSIZE)
    in_data  = array("H", samples)
    out_data = array("h", bytes(block_ct * channel_ct * PCM_BLOCKSIZE))

    for c in range(channel_ct):
        pcm_i = c

        for i in range(c * 2, block_ct * adpcm_size, adpcm_size):
            predictor = in_data[i]
            index     = in_data[i + 1]
            i += skip_size
            if endian == ">":
                predictor = (predictor >> 8) + ((predictor << 8) & 0xFF)
                index = (index >> 8) + ((index << 8) & 0xFF)

            if predictor & 32768:
                predictor -= pcm_mask

            out_data[pcm_i] = predictor
            pcm_i += channel_ct

            for j in range(i, i + code_skip_size, skip_size):
                codes = (in_data[j + 1] << 16) + in_data[j]

                for shift in code_shifts:
                    if   index > 88: index = 88
                    elif index < 0:  index = 0

                    code = codes >> shift
                    step = step_table[index]
                    index += index_table[code & 15]

                    if code & 8:
                        predictor -= ((step >> 1) + (code & 7) * step) >> 2
                        if predictor < -32768: predictor = -32768
                    else:
                        predictor += ((step >> 1) + (code & 15) * step) >> 2
                        if predictor >  32767: predictor =  32767

                    out_data[pcm_i] = predictor
                    pcm_i += channel_ct

    return out_data
