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


wind_body = Struct("tagdata", 
    h3_rawdata_ref("function_0"),
    h3_rawdata_ref("function_1"),
    h3_rawdata_ref("function_2"),
    h3_rawdata_ref("function_3"),
    h3_rawdata_ref("function_4"),
    Float("unknown"),
    h3_dependency("warp_bitmap"),
    ENDIAN=">", SIZE=120
    )


def get():
    return wind_def

wind_def = TagDef("wind",
    h3_blam_header('wind'),
    wind_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wind"], endian=">", tag_cls=H3Tag
    )