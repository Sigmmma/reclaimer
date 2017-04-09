from ..common_descs import *
from .objs.tag import H2VTag
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

LAMB_body = Struct("tagdata",
    ascii_str32("attachment marker name"),
    h2v_dependency("bitmaps", "bitm"),
    h2v_dependency("physics", "pphy"),

    Pad(80),
    BFloat("spring strength coefficient"),
    BFloat("falloff pixels"),
    BFloat("cutoff pixels"),

    Pad(40),
    h2_reflexive("vertices", vertex, 20),
    SIZE=208
    )

BLM__body = dict(LAMB_body)
BLM__body[0] = ascii_str_varlen("attachment marker name")
BLM__body[SIZE] = 180


def get():
    return ant__def

ant__def = TagDef("ant!",
    h2v_blam_header('ant!'),
    h2_tagdata_switch(
        (tbfd_container("tagdata", (LAMB_body, 208)), 'LAMB'),
        (tbfd_container("tagdata", (BLM__body, 180)), 'BLM_')
        ),
    ext=".antenna", endian="<", tag_cls=H2VTag
    )
