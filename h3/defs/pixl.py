############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


pixl_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


pixl_pixel_shader_unknown_2 = Struct("unknown_2", 
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


pixl_pixel_shader = Struct("pixel_shader", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    h3_reflexive("unknown_2", pixl_pixel_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=20, VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    UInt32("pixel_shader"),
    ENDIAN=">", SIZE=80
    )


pixl_meta_def = BlockDef("pixl", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", pixl_unknown_1),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    h3_reflexive("pixel_shaders", pixl_pixel_shader),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )