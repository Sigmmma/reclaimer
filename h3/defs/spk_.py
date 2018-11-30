############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Copypasta H2
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


spk__meta_def = BlockDef("spk_", 
    Float("almost_never"),
    Float("rarely"),
    Float("somewhat"),
    Float("often"),
    BytesRaw("unknown", SIZE=24, VISIBLE=False),
    TYPE=Struct, ENDIAN=">", SIZE=40
    )