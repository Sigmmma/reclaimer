from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


rwrd_meta_def = BlockDef("rwrd",
    Pad(76),
    TYPE=Struct, ENDIAN=">", SIZE=76
    )