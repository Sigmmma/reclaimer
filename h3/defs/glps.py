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


glps_unknown_0_unknown_0_unknown_1 = Struct("unknown_1", 
    UInt32("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


glps_unknown_0_unknown_0 = Struct("unknown_0", 
    UInt32("unknown_0", VISIBLE=False),
    reflexive("unknown_1", glps_unknown_0_unknown_0_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


glps_unknown_0 = Struct("unknown_0", 
    reflexive("unknown_0", glps_unknown_0_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


glps_pixel_shader_unknown_2 = Struct("unknown_2", 
    string_id_meta("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


glps_pixel_shader = Struct("pixel_shader", 
    rawdata_ref("unknown_0", VISIBLE=False),
    rawdata_ref("unknown_1", VISIBLE=False),
    reflexive("unknown_2", glps_pixel_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=24, VISIBLE=False),
    UInt32("pixel_shader"),
    ENDIAN=">", SIZE=80
    )


glps_meta_def = BlockDef("glps", 
    reflexive("unknown_0", glps_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    reflexive("pixel_shaders", glps_pixel_shader),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )