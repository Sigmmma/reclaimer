############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: -DeToX-
# 	Created layout of plugin
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


flck_meta_def = BlockDef("flck", 
    Pad(64),
    float_rad("perception_angle"),
    Pad(24),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )