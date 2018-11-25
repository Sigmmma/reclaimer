from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


hlsl_meta_def = BlockDef("hlsl",
    Pad(20),
    TYPE=Struct, ENDIAN=">", SIZE=20
    )