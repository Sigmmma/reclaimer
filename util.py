from os.path import sep as PATHDIV
from supyr_struct.defs.util import *
from math import log


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
