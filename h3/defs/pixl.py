############# Credits and version info #############
# Definition autogenerated from Assembly XML tag def
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


pixl_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


pixl_pixel_shader_unknown_2 = Struct("unknown_2", 
    string_id_meta("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


pixl_pixel_shader = Struct("pixel_shader", 
    rawdata_ref("unknown_0", VISIBLE=False),
    rawdata_ref("unknown_1", VISIBLE=False),
    reflexive("unknown_2", pixl_pixel_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=20, VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    UInt32("pixel_shader"),
    ENDIAN=">", SIZE=80
    )


pixl_meta_def = BlockDef("pixl", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    reflexive("unknown_1", pixl_unknown_1),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    reflexive("pixel_shaders", pixl_pixel_shader),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )