from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

wrot_animation_definition_anchor = (
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


wrot_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    SEnum16("anchor", *wrot_animation_definition_anchor),
    SInt16("unknown"),
    Float("custom_anchor_x"),
    Float("custom_anchor_y"),
    Float("rotation_amount"),
    Pad(12),
    ENDIAN=">", SIZE=32
    )


wrot_meta_def = BlockDef("wrot",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wrot_animation_definition),
    rawdata_ref("date"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )