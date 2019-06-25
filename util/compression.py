from math import log, sqrt, acos, sin


def decompress_quaternion48(word_0, word_1, word_2):
    '''Decompress a ones-signed 6byte quaternion to floats'''
    comp_rot = (word_2 & 0xFFff) | ((word_1 & 0xFFff)<<16) | ((word_0 & 0xFFff)<<32)
    w =  comp_rot & 4095
    k = (comp_rot >> 12) & 4095
    j = (comp_rot >> 24) & 4095
    i = (comp_rot >> 36) & 4095
    # avoid division by zero
    if i | j | k | w:
        if i & 0x800: i -= 4095
        if j & 0x800: j -= 4095
        if k & 0x800: k -= 4095
        if w & 0x800: w -= 4095
        length = sqrt(i**2 + j**2 + k**2 + w**2)
        return i / length, j / length, k / length, w / length
    return 0.0, 0.0, 0.0, 1.0


def compress_quaternion48(i, j, k, w):
    '''Compress normalized quaternion to a ones-signed 6byte representation'''
    comp_rot = 0
    nmag = i**2 + j**2 + k**2 + w**2
    # avoid division by zero
    if nmag:
        nmag = 2047.5 / sqrt(nmag)
        i = int(i*nmag) % 4095
        j = int(j*nmag) % 4095
        k = int(k*nmag) % 4095
        w = int(w*nmag) % 4095
        comp_rot = w | (k << 12) | (j << 24) | (i << 36)
    else:
        comp_rot = 2047

    return comp_rot>>32, (comp_rot>>16) & 0xFFff, comp_rot & 0xFFff


def decompress_normal32(n):
    i = (n&1023) / 1023
    j = ((n>>11)&1023) / 1023
    k = ((n>>22)&511) / 511
    if n&(1<<10): i -= 1.0
    if n&(1<<21): j -= 1.0
    if n&(1<<31): k -= 1.0

    return i, j, k


def compress_normal32(i, j, k):
    # original algorithm before shelly's optimization, kept for clarity

    #i = min(max(int(i*1023.5), -1023), 1023)
    #j = min(max(int(j*1023.5), -1023), 1023)
    #k = min(max(int(k*511.5),  -511),  511)
    #if i < 0: i += 2047
    #if j < 0: j += 2047
    #if k < 0: k += 1023
    #return i | (j << 11) | (k << 22)
    return ((int(i*1023.5) % 2047) |
            ((int(j*1023.5) % 2047) << 11) |
            ((int(k*511.5) % 1023) << 22))


def compress_normal32_normalize(i, j, k):
    nmag = 1023.5 / max(sqrt(i**2 + j**2 + k**2), 0.00000000001)
    return ((int(i*nmag) % 2047) |
            ((int(j*nmag) % 2047) << 11) |
            (((int(k*nmag) // 2) % 1023) << 22))


def lerp_blend_vectors(v0, v1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - r1
    return [a*r0 + b*r1 for a, b in zip(v0, v1)]


def nlerp_blend_quaternions(q0, q1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - ratio

    i0, j0, k0, w0 = q0
    i1, j1, k1, w1 = q1

    cos_half_theta = i0 * i1 + j0 * j1 + k0 * k1 + w0 * w1
    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        r1 = -r1

    return [i0*r0 + i1*r1, j0*r0 + j1*r1, k0*r0 + k1*r1, w0*r0 + w1*r1]


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
