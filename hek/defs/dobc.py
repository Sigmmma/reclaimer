from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get(): return dobc_def

detail_object_type = Struct("detail object type",
    ascii_str32("name"),
    SInt8("sequence index", SIDETIP="[0,15]"),
    Bool8("scale flags",
        ("interpolate color in hsv", 4),
        ("more colors", 8),
        ),
    #UInt8("unknown0", VISIBLE=False),
    #UInt8("unknown1", VISIBLE=False),
    Pad(2),
    float_zero_to_one("color override factor"),
    Pad(8),
    float_wu("near fade distance"),
    float_wu("far fade distance"),
    Float("size", SIDETIP="world units/pixel"),
    Pad(4),
    QStruct("minimum color", INCLUDE=rgb_float),
    QStruct("maximum color", INCLUDE=rgb_float),
    #QStruct("ambient color", INCLUDE=argb_byte),
    UInt32("ambient color", INCLUDE=argb_uint32),
    SIZE=96
    )

dobc_body = Struct("tagdata",
    SEnum16("anchor",
        "screen-facing",
        "viewer-facing",
        ),
    Pad(2),
    Float("global z offset",
        SIDETIP="applied to all these detail object so they dont float"),
    Pad(44),
    dependency("sprite plate", "bitm"),
    reflexive("detail object types", detail_object_type, 16,
        DYN_NAME_PATH='.name'),
    SIZE=128,
    )

dobc_def = TagDef("dobc",
    blam_header('dobc'),
    dobc_body,

    ext=".detail_object_collection", endian=">", tag_cls=HekTag
    )
