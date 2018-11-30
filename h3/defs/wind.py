############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


wind_meta_def = BlockDef("wind", 
    h3_rawdata_ref("function_0"),
    h3_rawdata_ref("function_1"),
    h3_rawdata_ref("function_2"),
    h3_rawdata_ref("function_3"),
    h3_rawdata_ref("function_4"),
    Float("unknown"),
    h3_dependency("warp_bitmap"),
    TYPE=Struct, ENDIAN=">", SIZE=120
    )