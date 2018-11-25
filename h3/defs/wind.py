from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wind_meta_def = BlockDef("wind",
    rawdata_ref("function"),
    rawdata_ref("function_1"),
    rawdata_ref("function_2"),
    rawdata_ref("function_3"),
    rawdata_ref("function_4"),
    Float("unknown"),
    dependency("warp_bitmap"),
    TYPE=Struct, ENDIAN=">", SIZE=120
    )