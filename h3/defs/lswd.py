############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: -DeToX-
# 	Mapped plugin structure a new.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


lswd_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=60, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=60
    )


lswd_meta_def = BlockDef("lswd", 
    BytesRaw("unknown_0", SIZE=8, VISIBLE=False),
    h3_dependency("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=52, VISIBLE=False),
    h3_reflexive("unknown_0", lswd_unknown_0),
    TYPE=Struct, ENDIAN=">", SIZE=88
    )