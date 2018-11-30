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


colo_color_table = Struct("color_table", 
    ascii_str32("string"),
    color_argb_float("color"),
    ENDIAN=">", SIZE=48
    )


colo_meta_def = BlockDef("colo", 
    h3_reflexive("color_table", colo_color_table),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )