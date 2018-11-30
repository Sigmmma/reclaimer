############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Standardizing
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


effg_unknown_unknown_2 = Struct("unknown_2", 
    SInt32("unknown_0"),
    SInt32("unknown_1"),
    Pad(4),
    SInt32("unknown_3"),
    ENDIAN=">", SIZE=16
    )


effg_unknown = Struct("unknown", 
    SInt32("unknown_0"),
    SInt32("unknown_1"),
    h3_reflexive("unknown_2", effg_unknown_unknown_2),
    ENDIAN=">", SIZE=20
    )


effg_meta_def = BlockDef("effg", 
    h3_reflexive("unknown", effg_unknown),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )