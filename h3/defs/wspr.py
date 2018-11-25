from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wspr_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    SInt16("sprite_index"),
    SInt16("sprite_index_1"),
    Pad(12),
    ENDIAN=">", SIZE=20
    )


wspr_meta_def = BlockDef("wspr",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wspr_animation_definition),
    rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )