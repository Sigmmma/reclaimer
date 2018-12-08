from ..common_descs import *
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
    h2_string_id("attachment marker name"),
    h2_dependency("bitmaps", "bitm"),
    h2_dependency("physics", "pphy"),

    Pad(80),
    Float("spring strength coefficient"),
    Float("falloff pixels"),
    Float("cutoff pixels"),

    Pad(40),
    h2_reflexive("vertices", vertex, 20),
    ENDIAN="<", SIZE=160
    )


def get():
    return ant__def

ant__def = TagDef("ant!",
    h2_blam_header('ant!'),
    ant__body,

    ext=".%s" % h2_tag_class_fcc_to_ext["ant!"], endian="<"
    )
