from math import ceil, log

from arbytmap.bitmap_io import get_pixel_bytes_size
from .constants import HALO3_SHARED_MAP_TYPES
from ..util import *


def get_virtual_dimension(bitm_fmt, dim, mip_level=0, tiled=False):
    dim = max(1, dim >> mip_level)
    if bitm_fmt in ("A8L8", "A8R8G8B8", "X8R8G8B8", "A4R4G4B4", "R5G6B5"):
        stride = 32
    elif bitm_fmt in ("A8", "L8", "AL8"):
        stride = 64
    else:
        stride = 128

    dim += ((stride - (dim % stride)) % stride)
    if mip_level != 0 and tiled:
        # first bitmap isnt padded
        dim = 2**int(ceil(log(dim, 2.0)))

    return dim


def get_h3_pixel_bytes_size(bitm_fmt, width, height, depth, mip, tiled=False):
    #if width <= 16 or height <= 16:
    #    tiled = False

    width = get_virtual_dimension(bitm_fmt, width, mip, tiled)
    height = get_virtual_dimension(bitm_fmt, height, mip, tiled)
    return get_pixel_bytes_size(bitm_fmt, width, height, depth)
