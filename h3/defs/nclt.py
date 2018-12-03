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


nclt_unknown_0 = Struct("unknown_0", 
    SInt32("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=28, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


nclt_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=16, VISIBLE=False),
    h3_dependency("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


nclt_body = Struct("tagdata", 
    h3_reflexive("unknown_0", nclt_unknown_0),
    h3_reflexive("unknown_1", nclt_unknown_1),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=28
    )


def get():
    return nclt_def

nclt_def = TagDef("nclt",
    h3_blam_header('nclt'),
    nclt_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["nclt"], endian=">", tag_cls=H3Tag
    )