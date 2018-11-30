############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	H2 Port
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


pphy_meta_def = BlockDef("pphy", 
    Bool32("flags", *unknown_flags_32),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=16, VISIBLE=False),
    Float("density", VISIBLE=False),
    Float("air_friction"),
    Float("water_friction"),
    Float("surface_friction"),
    Float("elasticity"),
    BytesRaw("unknown_4", SIZE=12, VISIBLE=False),
    TYPE=Struct, ENDIAN=">", SIZE=64
    )