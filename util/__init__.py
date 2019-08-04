from math import log

from os.path import sep as PATHDIV
from supyr_struct.util import *
from reclaimer.util import compression
from reclaimer.util import geometry
from reclaimer.util import matrices


POS_INF = float("inf")
NEG_INF = float("-inf")
RESERVED_WINDOWS_FILENAME_MAP = {}
INVALID_PATH_CHARS = set([str(i.to_bytes(1, 'little'), 'latin-1')
                          for i in (tuple(range(32)) +
                                    tuple(range(128, 256)))]
                         )
VALID_NUMERIC_CHARS = frozenset("0123456789")
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


def is_overlapping_ranges(range_0, range_1):
    assert isinstance(range_0, range)
    assert isinstance(range_1, range)
    assert range_0.step == 1
    assert range_1.step == 1
    return ((range_0.start in range_1 or range_0.stop in range_1) or
            (range_1.start in range_0 or range_1.stop in range_0))


def get_is_xbox_map(engine):
    return "xbox" in engine or engine in ("stubbs", "shadowrun_proto")


def float_to_str(f, max_sig_figs=7):
    if f == POS_INF:
        return "1000000000000000000000000000000000000000"
    elif f == NEG_INF:
        return "-1000000000000000000000000000000000000000"

    sig_figs = -1
    if abs(f) > 0:
        sig_figs = int(round(max_sig_figs - log(abs(f), 10) - 1))

    if sig_figs < 0:
        return str(f).split(".")[0]

    str_float = ("%" + (".%sf" % sig_figs)) % f
    if "." in str_float:
        return str_float.rstrip("0").rstrip(".")
    return str_float


def float_to_str_truncate(f, sig_figs=7):
    if f == POS_INF:
        str_float = "1000000000000000000000000000000000000000"
    elif f == NEG_INF:
        str_float = "-1000000000000000000000000000000000000000"
    else:
        str_float = ("%" + (".%sf" % sig_figs)) % f

    float_pieces = str_float.split(".", 1)
    if len(float_pieces) == 1:
        remainder = "0" * sig_figs
    else:
        remainder = float_pieces[1] + "0" * (sig_figs - len(float_pieces[1]))

    return "%s.%s" % (float_pieces[0], remainder[: sig_figs])


def parse_jm_int(string):
    try:
        i = 1 if string[0] == "-" else 0
        check = VALID_NUMERIC_CHARS
        while i < len(string):
            if string[i] not in check:
                break
            i += 1
        return int(string[: i])
    except Exception:
        return 0


def parse_jm_float(string):
    try:
        i = 1 if string[0] == "-" else 0
        check = VALID_NUMERIC_CHARS
        found_period = False
        while i < len(string):
            c = string[i]
            if c == "." and not found_period:
                found_period = True
            elif c not in check:
                break
            i += 1
        return float(string[: i])
    except Exception:
        return 0.0


def is_valid_ascii_name_str(string):
    if not string:
        return True

    try:
        string_bytes = set(string.encode("latin-1"))
    except Exception:
        return False

    if max(string_bytes) > 127:
        return False

    for i in tuple(range(8)) + tuple(range(14, 32)):
        if i in string_bytes:
            return False
    return True
