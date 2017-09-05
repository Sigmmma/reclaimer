from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

vertex = Struct("vertex",
    Float("spring strength coefficient"),

    Pad(24),
    yp_float_rad("angles"),  # radians
    float_wu("length"),
    SInt16("sequence index"),

    Pad(2),
    QStruct("color", INCLUDE=argb_float),
    QStruct("lod color", INCLUDE=argb_float),
    SIZE=128
    )

ant__body = Struct("tagdata",
    ascii_str32("attachment marker name"),
    dependency("bitmaps", "bitm"),
    dependency("physics", "pphy"),

    Pad(80),
    Float("spring strength coefficient"),
    Float("falloff pixels"),
    Float("cutoff pixels"),

    Pad(40),
    reflexive("vertices", vertex, 20),
    SIZE=208
    )


def get():
    return ant__def

ant__def = TagDef("ant!",
    blam_header('ant!'),
    ant__body,

    ext=".antenna", endian=">", tag_cls=HekTag
    )
