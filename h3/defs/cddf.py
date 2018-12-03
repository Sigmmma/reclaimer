############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
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
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


cddf_body = Struct("tagdata", 
    Float("apply_damage_scale"),
    Float("apply_recoil_damage_scale"),
    QStruct("damage_acceleration", INCLUDE=from_to),
    Float("damage_scale_min_0"),
    Float("damage_scale_min_1"),
    QStruct("recoil_damage_acceleration", INCLUDE=from_to),
    QStruct("recoil_damage_scale", INCLUDE=from_to),
    ENDIAN=">", SIZE=40
    )


def get():
    return cddf_def

cddf_def = TagDef("cddf",
    h3_blam_header('cddf'),
    cddf_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["cddf"], endian=">", tag_cls=H3Tag
    )