############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Woo
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


sgp__meta_def = BlockDef("sgp_", 
    h3_dependency("underwater_environment"),
    h3_dependency("underwater_loop"),
    BytesRaw("unknown", SIZE=8, VISIBLE=False),
    h3_dependency("enter_underater"),
    h3_dependency("exit_underwater"),
    TYPE=Struct, ENDIAN=">", SIZE=72
    )