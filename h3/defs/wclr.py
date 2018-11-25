from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wclr_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    color_argb_float("color"),
    Pad(12),
    ENDIAN=">", SIZE=32
    )


wclr_meta_def = BlockDef("wclr",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wclr_animation_definition),
    rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )