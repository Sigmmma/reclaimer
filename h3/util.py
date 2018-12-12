from .constants import HALO3_SHARED_MAP_TYPES
from ..util import *


def get_virtual_dimension(bitm_fmt, dim, mip_level=0):
    stride = 128
    if bitm_fmt in ("A8", "L8", "AL8", "A8L8", "A8R8G8B8",
                    "A4R4G4B4", "R5G6B5"):
        stride = 32
    dim = dim >> mip_level
    return dim + ((stride - (dim % stride)) % stride)
