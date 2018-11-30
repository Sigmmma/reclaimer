############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: -DeToX-
# 	Created layout of plugin
# revision: 2		author: Lord Zedd
# 	Done
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


chmt_lighting_variable = Struct("lighting_variable", 
    Float("lightmap_brightness_offset"),
    ENDIAN=">", SIZE=4
    )


chmt_meta_def = BlockDef("chmt", 
    h3_reflexive("lighting_variables", chmt_lighting_variable),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )