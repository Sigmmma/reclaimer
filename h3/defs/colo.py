############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


colo_color_table = Struct("color_table", 
    ascii_str32("string"),
    color_argb_float("color"),
    ENDIAN=">", SIZE=48
    )


colo_body = Struct("tagdata", 
    h3_reflexive("color_table", colo_color_table),
    ENDIAN=">", SIZE=12
    )


def get():
    return colo_def

colo_def = TagDef("colo",
    h3_blam_header('colo'),
    colo_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["colo"], endian=">", tag_cls=H3Tag
    )