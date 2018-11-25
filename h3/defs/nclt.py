from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


nclt_unknown = Struct("unknown",
    SInt32("unknown"),
    Pad(28),
    ENDIAN=">", SIZE=32
    )


nclt_unknown_1 = Struct("unknown_1",
    Pad(16),
    dependency("unknown_1"),
    ENDIAN=">", SIZE=32
    )


nclt_meta_def = BlockDef("nclt",
    reflexive("unknown", nclt_unknown),
    reflexive("unknown_1", nclt_unknown_1),
    Pad(4),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )