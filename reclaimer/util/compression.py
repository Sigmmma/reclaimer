#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import sqrt


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
        length = 1.0 / sqrt(i**2 + j**2 + k**2 + w**2)
        return i * length, j * length, k * length, w * length
    return 0.0, 0.0, 0.0, 1.0


def compress_quaternion48(i, j, k, w):
    '''Compress normalized quaternion to a ones-signed 6byte representation'''
    comp_rot = 0
    nmag = i**2 + j**2 + k**2 + w**2
    # avoid division by zero
    if nmag:
        nmag = 2047 / sqrt(nmag)
        i = int(round(i*nmag)) % 4095
        j = int(round(j*nmag)) % 4095
        k = int(round(k*nmag)) % 4095
        w = int(round(w*nmag)) % 4095
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
    i = min(max(i, -1.0), 1.0)
    j = min(max(j, -1.0), 1.0)
    k = min(max(k, -1.0), 1.0)
    # original algorithm before shelly's optimization, kept for clarity
    #if i < 0: i += 2047
    #if j < 0: j += 2047
    #if k < 0: k += 1023
    #return i | (j << 11) | (k << 22)
    return ((int(round(i*1023)) % 2047) |
            ((int(round(j*1023)) % 2047) << 11) |
            ((int(round(k*511)) % 1023) << 22))


#uncomp_norm = [.333, -.75, 1]
#nmag = sqrt(sum(uncomp_norm[i]**2 for i in range(3)))
#uncomp_norm = [val / nmag for val in uncomp_norm]
#comp_norm = compress_normal32(*uncomp_norm)
#print(uncomp_norm)
#print(comp_norm)
#print(decompress_normal32(comp_norm))

#orig = (0xdab8, 0x67f1, 0x2fff)
#recomp = compress_quaternion48(*decompress_quaternion48(*orig))
#print(orig)
#print(recomp)
#print(decompress_quaternion48(*orig))
#print(decompress_quaternion48(*recomp))
