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


rmt2_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


rmt2_unknown_2 = Struct("unknown_2", 
    BytesRaw("unknown", SIZE=28, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=28
    )


rmt2_unknown_3 = Struct("unknown_3", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


rmt2_argument = Struct("argument", 
    h3_string_id("name"),
    ENDIAN=">", SIZE=4
    )


rmt2_unknown_4 = Struct("unknown_4", 
    h3_string_id("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


rmt2_unknown_5 = Struct("unknown_5", 
    h3_string_id("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


rmt2_shader_map = Struct("shader_map", 
    h3_string_id("name"),
    ENDIAN=">", SIZE=4
    )


rmt2_body = Struct("tagdata", 
    h3_dependency("vertex_shader"),
    h3_dependency("pixel_shader"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", rmt2_unknown_1),
    h3_reflexive("unknown_2", rmt2_unknown_2),
    h3_reflexive("unknown_3", rmt2_unknown_3),
    h3_reflexive("arguments", rmt2_argument),
    h3_reflexive("unknown_4", rmt2_unknown_4),
    h3_reflexive("unknown_5", rmt2_unknown_5),
    h3_reflexive("shader_maps", rmt2_shader_map),
    BytesRaw("unknown_6", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=132
    )


def get():
    return rmt2_def

rmt2_def = TagDef("rmt2",
    h3_blam_header('rmt2'),
    rmt2_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["rmt2"], endian=">", tag_cls=H3Tag
    )