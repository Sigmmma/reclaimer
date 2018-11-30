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


shit_meta_def = BlockDef("shit", 
    h3_dependency("unknown_0"),
    h3_dependency("unknown_1"),
    Array("unknown_array", SIZE=9, SUB_STRUCT=Float("unknown"), VISIBLE=False),
    color_rgb_float("color_0"),
    Float("unknown_2", VISIBLE=False),
    color_rgb_float("color_1"),
    Float("unknown_3", VISIBLE=False),
    color_rgb_float("color_2"),
    Float("unknown_4", VISIBLE=False),
    color_rgb_float("color_3"),
    Float("unknown_5", VISIBLE=False),
    color_rgb_float("color_4"),
    Float("unknown_6", VISIBLE=False),
    color_rgb_float("color_5"),
    Float("unknown_7", VISIBLE=False),
    TYPE=Struct, ENDIAN=">", SIZE=164
    )