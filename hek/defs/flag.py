from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get(): return flag_def

attachment_point = Struct("attachment point",
    SInt16("height to next attachment", SIDETIP="vertices"),
    Pad(18),
    ascii_str32("marker name"),
    )

flag_body = Struct("tagdata",
    Pad(4),
    SEnum16("trailing edge shape",
        "flat",
        "concave triangular",
        "convex triangular",
        "trapezoid short top",
        "trapezoid short bottom",
        ),

    SInt16("trailing edge shape offset", SIDETIP="vertices"),
    SEnum16("attached edge shape",
        "flat",
        "concave triangular",
        ),
    Pad(2),
    SInt16("width", SIDETIP="vertices"),
    SInt16("height", SIDETIP="vertices"),

    float_wu("cell width"),
    float_wu("cell height"),

    dependency("red flag shader", valid_shaders),
    dependency("physics", "pphy"),

    float_wu_sec("wind noise"),
    Pad(8),
    dependency("blue flag shader", valid_shaders),
    reflexive("attachment points", attachment_point, 4,
        DYN_NAME_PATH='.marker_name'),
    SIZE=96,
    )

flag_def = TagDef("flag",
    blam_header('flag'),
    flag_body,

    ext=".flag", endian=">", tag_cls=HekTag
    )
