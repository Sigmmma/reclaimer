from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


control_point = Struct("control point",
    Struct("position", ijk_float),
    Struct("orientation", ijkw_float),
    SIZE=60,
    )

trak_body = Struct("tagdata",
    Pad(4),
    reflexive("control points", control_point, 16),
    SIZE=48,
    )


def get():
    return trak_def

trak_def = TagDef("trak",
    blam_header('trak', 2),
    trak_body,

    ext=".camera_track", endian=">"
    )
