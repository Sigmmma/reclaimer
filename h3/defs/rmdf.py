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


rmdf_method_shader_option = Struct("shader_option", 
    h3_string_id("type"),
    h3_dependency("option"),
    h3_string_id("unknown_0", VISIBLE=False),
    h3_string_id("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=28
    )


rmdf_method = Struct("method", 
    h3_string_id("type"),
    h3_reflexive("shader_options", rmdf_method_shader_option),
    h3_string_id("unknown_0", VISIBLE=False),
    h3_string_id("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


rmdf_unknown_1_unknown_1_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


rmdf_unknown_1_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", rmdf_unknown_1_unknown_1_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


rmdf_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", rmdf_unknown_1_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


rmdf_unknown_2 = Struct("unknown_2", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


rmdf_body = Struct("tagdata", 
    h3_dependency("unknown_0", VISIBLE=False),
    h3_reflexive("methods", rmdf_method),
    h3_reflexive("unknown_1", rmdf_unknown_1),
    h3_reflexive("unknown_2", rmdf_unknown_2),
    h3_dependency("unknown_3", VISIBLE=False),
    h3_dependency("unknown_4", VISIBLE=False),
    BytesRaw("unknown_5", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=92
    )


def get():
    return rmdf_def

rmdf_def = TagDef("rmdf",
    h3_blam_header('rmdf'),
    rmdf_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["rmdf"], endian=">", tag_cls=H3Tag
    )