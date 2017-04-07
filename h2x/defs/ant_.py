from ..common_descs import *
from .objs.tag import H2XTag
from supyr_struct.defs.tag_def import TagDef

vertex = Struct("vertex",
    BFloat("spring strength coefficient"),

    Pad(24),
    yp_float_rad("angles"),  # radians
    float_wu("length"),
    BSInt16("sequence index"),

    Pad(2),
    QStruct("color", INCLUDE=argb_float),
    QStruct("lod color", INCLUDE=argb_float),
    SIZE=128
    )

ant__body = Struct("tagdata",
    ascii_str32("attachment marker name"),
    h2xdependency("bitmaps", "bitm"),
    h2xdependency("physics", "pphy"),

    Pad(80),
    BFloat("spring strength coefficient"),
    BFloat("falloff pixels"),
    BFloat("cutoff pixels"),

    Pad(40),
    h2xreflexive("vertices", vertex, 20),
    SIZE=208
    )


def get():
    return ant__def

ant__def = TagDef("ant!",
    h2xblam_header('ant!'),
    ant__body,

    ext=".antenna", endian="<", tag_cls=H2XTag
    )
