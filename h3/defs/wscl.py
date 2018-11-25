from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

wscl_animation_definition_anchor = (
    "custom",
    "center",
    "top_center",
    "bottom_center",
    "left_center",
    "right_center",
    "top_left",
    "top_right",
    "bottom_right",
    "bottom_left",
    )


wscl_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    SEnum16("anchor", *wscl_animation_definition_anchor),
    SInt16("unknown"),
    Float("custom_anchor_x"),
    Float("custom_anchor_y"),
    Float("x_scale"),
    Float("y_scale"),
    Pad(12),
    ENDIAN=">", SIZE=36
    )


wscl_meta_def = BlockDef("wscl",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wscl_animation_definition),
    rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )