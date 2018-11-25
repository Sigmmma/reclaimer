from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


sgp__meta_def = BlockDef("sgp!",
    dependency("underwater_environment"),
    dependency("underwater_loop"),
    Pad(8),
    dependency("enter_underater"),
    dependency("exit_underwater"),
    TYPE=Struct, ENDIAN=">", SIZE=72
    )
