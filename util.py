from os.path import sep as PATHDIV
from supyr_struct.defs.util import *
from math import log, sqrt


POS_INF = float("inf")
NEG_INF = float("-inf")
RESERVED_WINDOWS_FILENAME_MAP = {}
INVALID_PATH_CHARS = set([str(i.to_bytes(1, 'little'), 'ascii')
                          for i in range(32)])
for name in ('CON', 'PRN', 'AUX', 'NUL'):
    RESERVED_WINDOWS_FILENAME_MAP[name] = '_' + name
for i in range(1, 9):
    RESERVED_WINDOWS_FILENAME_MAP['COM%s' % i] = '_COM%s' % i
    RESERVED_WINDOWS_FILENAME_MAP['LPT%s' % i] = '_LPT%s' % i
INVALID_PATH_CHARS.update('<>:"|?*')


def is_reserved_tag(tag_index_ref):
    return (tag_index_ref.id == 0xFFffFFff and
            tag_index_ref.class_1.data == 0xFFFFFFFF)


def is_protected_tag(tagpath):
    return not tagpath or tagpath in RESERVED_WINDOWS_FILENAME_MAP or (
        not INVALID_PATH_CHARS.isdisjoint(set(tagpath)))


def get_is_xbox_map(engine):
    return "xbox" in engine or engine in ("stubbs", "shadowrun_proto")


def float_to_str(f, max_sig_figs=7):
    if f == POS_INF:
        return "1000000000000000000000000000000000000000"
    elif f == NEG_INF:
        return "-1000000000000000000000000000000000000000"

    sig_figs = -1
    if abs(f) > 0:
        sig_figs = int(round(max_sig_figs - log(abs(f), 10)))

    if sig_figs < 0:
        return str(f).split(".")[0]
    return (("%" + (".%sf" % sig_figs)) % f).rstrip("0").rstrip(".")


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


#uncomp_norm = [.333, -.75, 1]
#nmag = sqrt(sum(uncomp_norm[i]**2 for i in range(3)))
#uncomp_norm = [val / nmag for val in uncomp_norm]
#comp_norm = compress_normal32(*uncomp_norm)
#print(uncomp_norm)
#print(comp_norm)
#print(decompress_normal32(comp_norm))
