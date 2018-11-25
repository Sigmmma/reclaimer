from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wfon_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    SInt16("font_index"),
    SInt16("unknown"),
    Pad(12),
    ENDIAN=">", SIZE=20
    )


wfon_meta_def = BlockDef("wfon",
    Bool32("animation_flags",
        "loops",
        ),
    reflexive("animation_definition", wfon_animation_definition),
    rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )