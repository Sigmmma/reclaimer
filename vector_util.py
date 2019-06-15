from math import log, sqrt, acos, sin


def decompress_quaternion48(word_0, word_1, word_2):
    comp_rot = (word_2 & 0xFFff) | ((word_1 & 0xFFff)<<16) | ((word_0 & 0xFFff)<<32)
    w =  comp_rot & 2047
    k = (comp_rot >> 12) & 2047
    j = (comp_rot >> 24) & 2047
    i = (comp_rot >> 36) & 2047
    # avoid division by zero
    if i | j | k | w:
        if comp_rot & 0x800:          w = w - 2047
        if comp_rot & 0x800000:       k = k - 2047
        if comp_rot & 0x800000000:    j = j - 2047
        if comp_rot & 0x800000000000: i = i - 2047
        length = sqrt(i**2 + j**2 + k**2 + w**2)
        return i / length, j / length, k / length, w / length
    return 0.0, 0.0, 0.0, 1.0


def decompress_normal32(n):
    ni = (n&1023) / 1023
    nj = ((n>>11)&1023) / 1023
    nk = ((n>>22)&511) / 511
    if n&(1<<10): ni = ni - 1.0
    if n&(1<<21): nj = nj - 1.0
    if n&(1<<31): nk = nk - 1.0

    return ni, nj, nk


def compress_normal32(ni, nj, nk):
    # original algorithm before shelly's optimization, kept for clarity

    #ni = min(max(int(ni*1023.5), -1023), 1023)
    #nj = min(max(int(nj*1023.5), -1023), 1023)
    #nk = min(max(int(nk*511.5),  -511),  511)
    #if ni < 0: ni += 2047
    #if nj < 0: nj += 2047
    #if nk < 0: nk += 1023
    #return ni | (nj << 11) | (nk << 22)
    return ((int(ni*1023.5) % 2047) |
            ((int(nj*1023.5) % 2047) << 11) |
            ((int(nk*511.5) % 1023) << 22))


def compress_normal32_normalize(ni, nj, nk):
    nmag = 1023.5 / max(sqrt(ni**2 + nj**2 + nk**2), 0.00000000001)
    return ((int(ni*nmag) % 2047) |
            ((int(nj*nmag) % 2047) << 11) |
            (((int(nk*nmag) // 2) % 1023) << 22))


def nlerp_blend_normalized_vectors(vector_0, vector_1, ratio):
    ratio = max(0.0, min(1.0, ratio))
    assert len(vector_0) == len(vector_1)

    return [(v0 * (1.0 - ratio) / v0_len) + (v1 * ratio / v1_len)
            for v0, v1 in zip(vector_0, vector_1)]


def slerp_blend_normalized_vectors(vector_0, vector_1, ratio):
    ratio = max(0.0, min(1.0, ratio))
    assert len(vector_0) == len(vector_1)
    
    cos_half_theta = sqrt(sum(v0 * v1 for v0, v1 in zip(vector_0, vector_1)))
    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        vector_1 = [-v for v in vector_1]
        cos_half_theta *= -1

    half_theta = 0.0
    if abs(cos_half_theta) < 1.0:
        half_theta = acos(cos_half_theta)

    # angle is not well defined in floating point at this point
    if cos_half_theta > 0.9999999:
        r0 = 1.0 - ratio
        r1 = ratio
    else:
        sin_half_theta = sqrt(max(1 - cos_half_theta**2, 0))
        r0 = sin((1.0 - ratio) * half_theta) / sin_half_theta
        r1 = sin(ratio * half_theta) / sin_half_theta

    return [v0 * r0 + v1 * r1 for v0, v1 in zip(vector_0, vector_1)]


def nlerp_blend_vectors(vector_0, vector_1, ratio):
    ratio = max(0.0, min(1.0, ratio))
    assert len(vector_0) == len(vector_1)

    v0_len = sqrt(sum(v**2 for v in vector_0))
    v1_len = sqrt(sum(v**2 for v in vector_1))
    return [v0 * (1.0 - ratio) / v0_len + v1 * ratio / v1_len
            for v0, v1 in zip(vector_0, vector_1)]


def slerp_blend_vectors(vector_0, vector_1, ratio):
    ratio = max(0.0, min(1.0, ratio))
    assert len(vector_0) == len(vector_1)

    v0_len = sqrt(sum(v**2 for v in vector_0))
    v1_len = sqrt(sum(v**2 for v in vector_1))
    
    cos_half_theta = sqrt(sum(v0 * v1 for v0, v1 in zip(vector_0, vector_1)))
    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        vector_1 = [-v for v in vector_1]
        cos_half_theta *= -1

    half_theta = 0.0
    if abs(cos_half_theta) < 1.0:
        half_theta = acos(cos_half_theta)

    # angle is not well defined in floating point at this point
    if cos_half_theta > 0.9999999:
        r0 = 1.0 - ratio
        r1 = ratio
    else:
        sin_half_theta = sqrt(max(1 - cos_half_theta**2, 0))
        r0 = sin((1.0 - ratio) * half_theta) / sin_half_theta
        r1 = sin(ratio * half_theta) / sin_half_theta

    r0 /= v0_len
    r1 /= v1_len

    return [v0 * r0 + v1 * r1 for v0, v1 in zip(vector_0, vector_1)]


#uncomp_norm = [.333, -.75, 1]
#nmag = sqrt(sum(uncomp_norm[i]**2 for i in range(3)))
#uncomp_norm = [val / nmag for val in uncomp_norm]
#comp_norm = compress_normal32(*uncomp_norm)
#print(uncomp_norm)
#print(comp_norm)
#print(decompress_normal32(comp_norm))
