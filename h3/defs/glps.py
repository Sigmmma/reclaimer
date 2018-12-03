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


glps_unknown_0_unknown_0_unknown_1 = Struct("unknown_1", 
    UInt32("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


glps_unknown_0_unknown_0 = Struct("unknown_0", 
    UInt32("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", glps_unknown_0_unknown_0_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


glps_unknown_0 = Struct("unknown_0", 
    h3_reflexive("unknown_0", glps_unknown_0_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


glps_pixel_shader_unknown_2 = Struct("unknown_2", 
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


glps_pixel_shader = Struct("pixel_shader", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    h3_reflexive("unknown_2", glps_pixel_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=24, VISIBLE=False),
    UInt32("pixel_shader"),
    ENDIAN=">", SIZE=80
    )


glps_body = Struct("tagdata", 
    h3_reflexive("unknown_0", glps_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("pixel_shaders", glps_pixel_shader),
    ENDIAN=">", SIZE=28
    )


def get():
    return glps_def

glps_def = TagDef("glps",
    h3_blam_header('glps'),
    glps_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["glps"], endian=">", tag_cls=H3Tag
    )