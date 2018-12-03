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


rmop_unknown = Struct("unknown", 
    h3_string_id("type"),
    BytesRaw("unknown_0", SIZE=8, VISIBLE=False),
    h3_dependency("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=44, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=72
    )


rmop_body = Struct("tagdata", 
    h3_reflexive("unknown", rmop_unknown),
    ENDIAN=">", SIZE=12
    )


def get():
    return rmop_def

rmop_def = TagDef("rmop",
    h3_blam_header('rmop'),
    rmop_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["rmop"], endian=">", tag_cls=H3Tag
    )