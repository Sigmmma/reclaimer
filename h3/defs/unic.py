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


unic_body = Struct("tagdata", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_rawdata_ref("unknown_1"),
    UInt32("strings"),
    ENDIAN=">", SIZE=80
    )


def get():
    return unic_def

unic_def = TagDef("unic",
    h3_blam_header('unic'),
    unic_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["unic"], endian=">", tag_cls=H3Tag
    )