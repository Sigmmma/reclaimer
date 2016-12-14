from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return dobc_def

detail_object_type = Struct("detail object type",
    ascii_str32("name"),
    SInt8("sequence index", SIDETIP="[0,15]"),
    Bool8("scale flags",
        ("interpolate color in hsv", 4),
        ("more colors", 8),
        ),
    Pad(2),
    float_zero_to_one("color override factor"),
    Pad(8),
    float_wu("near fade distance"),
    float_wu("far fade distance"),
    BFloat("size", SIDETIP="world units/pixel"),
    Pad(4),
    QStruct("minimum color", INCLUDE=rgb_float),
    QStruct("maximum color", INCLUDE=rgb_float),
    QStruct("ambient color", INCLUDE=argb_byte),
    SIZE=96
    )

dobc_body = Struct("tagdata",
    BSEnum16("anchor",
        "screen-facing",
        "viewer-facing",
        ),
    Pad(2),
    BFloat("global z offset",
        SIDETIP="applied to all these detail object so they dont float"),
    Pad(44),
    dependency("sprite plate", "bitm"),
    reflexive("detail object types", detail_object_type, 16),
    SIZE=128,
    )

dobc_def = TagDef("dobc",
    blam_header('dobc'),
    dobc_body,

    ext=".detail_object_collection", endian=">"
    )
