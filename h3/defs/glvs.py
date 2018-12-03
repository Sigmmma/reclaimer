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


glvs_unknown_0_unknown_unknown_0_unknown_1 = Struct("unknown_1", 
    UInt32("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


glvs_unknown_0_unknown_unknown_0 = Struct("unknown_0", 
    UInt32("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", glvs_unknown_0_unknown_unknown_0_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


glvs_unknown_0_unknown = Struct("unknown", 
    h3_reflexive("unknown_0", glvs_unknown_0_unknown_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


glvs_unknown_0 = Struct("unknown_0", 
    h3_reflexive("unknown", glvs_unknown_0_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


glvs_vertex_shader_unknown_2 = Struct("unknown_2", 
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


glvs_vertex_shader = Struct("vertex_shader", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    h3_reflexive("unknown_2", glvs_vertex_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=24, VISIBLE=False),
    UInt32("vertex_shader"),
    ENDIAN=">", SIZE=80
    )


glvs_body = Struct("tagdata", 
    h3_reflexive("unknown_0", glvs_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("vertex_shaders", glvs_vertex_shader),
    ENDIAN=">", SIZE=28
    )


def get():
    return glvs_def

glvs_def = TagDef("glvs",
    h3_blam_header('glvs'),
    glvs_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["glvs"], endian=">", tag_cls=H3Tag
    )