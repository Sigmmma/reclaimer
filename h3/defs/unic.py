from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


unic_meta_def = BlockDef("unic",
    Pad(12),
    rawdata_ref("unknown_1"),
    UInt32("strings"),
    TYPE=Struct, ENDIAN=">", SIZE=80
    )