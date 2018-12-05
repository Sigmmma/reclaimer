from .constants import HALO2_MAP_TYPES


def split_raw_pointer(ptr):
    return ptr & 0x3FffFFff, HALO2_MAP_TYPES[(ptr>>30)&3]
