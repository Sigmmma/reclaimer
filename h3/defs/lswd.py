from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


lswd_unknown_0 = Struct("unknown_0",
    Pad(60),
    ENDIAN=">", SIZE=60
    )


lswd_meta_def = BlockDef("lswd",
    Pad(8),
    dependency("unknown_1"),
    Pad(52),
    reflexive("unknown_0", lswd_unknown_0),
    TYPE=Struct, ENDIAN=">", SIZE=88
    )