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


cddf_meta_def = BlockDef("cddf", 
    Float("apply_damage_scale"),
    Float("apply_recoil_damage_scale"),
    QStruct("damage_acceleration", INCLUDE=from_to),
    Float("damage_scale_min_0"),
    Float("damage_scale_min_1"),
    QStruct("recoil_damage_acceleration", INCLUDE=from_to),
    QStruct("recoil_damage_scale", INCLUDE=from_to),
    TYPE=Struct, ENDIAN=">", SIZE=40
    )