from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


effg_unknown_unknown_2 = Struct("unknown_2",
    SInt32("unknown"),
    SInt32("unknown_1"),
    Pad(4),
    SInt32("unknown_3"),
    ENDIAN=">", SIZE=16
    )


effg_unknown = Struct("unknown",
    SInt32("unknown"),
    SInt32("unknown_1"),
    reflexive("unknown_2", effg_unknown_unknown_2),
    ENDIAN=">", SIZE=20
    )


effg_meta_def = BlockDef("effg",
    reflexive("unknown", effg_unknown),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )