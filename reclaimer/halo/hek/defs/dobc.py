from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return dobc_def

detail_object_type = Struct("detail object type",
    StrLatin1("name", SIZE=32),
    SInt8("sequence index"),
    Bool8("scale flags",
        ("interpolate color in hsv", 4),
        ("more colors", 8),
        ),
    Pad(2),
    BFloat("color override factor"),
    Pad(8),
    BFloat("near fade distance"),
    BFloat("far fade distance"),
    BFloat("size"),
    Pad(4),
    Struct("minimum color", INCLUDE=rgb_float),
    Struct("maximum color", INCLUDE=rgb_float),
    Struct("ambient color", INCLUDE=argb_byte),
    SIZE=104
    )

dobc_body = Struct("tagdata",
    BSEnum16("anchor",
        "screen-facing",
        "viewer-facing",
        ),
    Pad(2),
    BFloat("global z offset"), #applied to all detail object so they dont float
    Pad(44),
    dependency("sprite plate", valid_bitmaps),
    reflexive("detail object types", detail_object_type, 16),
    SIZE=128,
    )

dobc_def = TagDef("dobc",
    blam_header('dobc'),
    dobc_body,

    ext=".detail_object_collection", endian=">"
    )
