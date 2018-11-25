from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wtuv_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    Float("coordinate_x"),
    Float("coordinate_y"),
    Pad(12),
    ENDIAN=">", SIZE=24
    )


wtuv_meta_def = BlockDef("wtuv",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wtuv_animation_definition),
    rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )