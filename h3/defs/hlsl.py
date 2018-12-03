############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: -DeToX-
# 	Mapped plugin structure a new.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


hlsl_body = Struct("tagdata", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


def get():
    return hlsl_def

hlsl_def = TagDef("hlsl",
    h3_blam_header('hlsl'),
    hlsl_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["hlsl"], endian=">", tag_cls=H3Tag
    )