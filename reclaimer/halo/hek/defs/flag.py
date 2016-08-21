from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return ant__def

antenna_vertex = Struct("antenna vertex",
    BFloat("spring strength coefficient"),
    Pad(24),
    Struct("angles", INCLUDE=yp_float),  # measured in radians
    BFloat("length"),
    BSInt16("sequence index"),
    Pad(2),
    Struct("color", INCLUDE=argb_float),
    Struct("lod color", INCLUDE=argb_float),
    SIZE=128
    )

ant__body = Struct("tagdata",
    StrLatin1("name", SIZE=32),
    dependency("bitmaps", valid_bitmaps),
    dependency("physics", valid_point_physics),
    Pad(80),

    BFloat("spring strength coefficient"),
    BFloat("falloff pixels"),
    BFloat("cutoff pixels"),
    Pad(40),
    reflexive("vertices", antenna_vertex, 20),
    SIZE=208,
    )

ant__def = TagDef("ant!",
    blam_header('ant!'),
    ant__body,

    ext=".antenna", endian=">"
    )
