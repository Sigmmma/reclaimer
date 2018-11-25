from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wpos_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    Float("x_position"),
    Float("y_position"),
    Float("z_position"),
    Pad(12),
    ENDIAN=">", SIZE=28
    )


wpos_meta_def = BlockDef("wpos",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wpos_animation_definition),
    rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )