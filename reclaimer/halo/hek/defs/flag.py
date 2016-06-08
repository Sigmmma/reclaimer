from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get(): return flag_def

attachment_point = Struct("attachment point",
    BSInt16("height to next attachment"),
    Pad(18),
    StrLatin1("marker name", SIZE=32),
    )

flag_body = Struct("tagdata",
    Pad(4),
    BSEnum16("trailing edge shape",
        "flat",
        "concave triangular",
        "convex triangular",
        "trapezoid short top",
        "trapezoid short bottom",
        ),

    BSInt16("trailing edge shape offset"),
    BSEnum16("attached edge shape",
        "flat",
        "concave triangular",
        ),
    Pad(2),
    BSInt16("width"),
    BSInt16("height"),

    BFloat("cell width"),
    BFloat("cell height"),

    dependency("red flag shader", valid_shaders),
    dependency("physics", valid_point_physics),

    BFloat("wind noise"),
    Pad(8),
    dependency("blue flag shader", valid_shaders),
    reflexive("attachment points", attachment_point, 4),
    SIZE=96,
    )

flag_def = TagDef(
    blam_header('flag'),
    flag_body,
    
    NAME="flag",
    
    ext=".flag", def_id="flag", endian=">"
    )
