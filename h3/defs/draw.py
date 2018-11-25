from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


draw_meta_def = BlockDef("draw",
    Pad(4),
    TYPE=Struct, ENDIAN=">", SIZE=4
    )