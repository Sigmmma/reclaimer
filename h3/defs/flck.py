from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


flck_meta_def = BlockDef("flck",
    Pad(64),
    float_rad("perception_angle"),
    Pad(24),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )