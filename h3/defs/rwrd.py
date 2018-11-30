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


rwrd_meta_def = BlockDef("rwrd", 
    BytesRaw("unknown", SIZE=76, VISIBLE=False),
    TYPE=Struct, ENDIAN=">", SIZE=76
    )