############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Basically done.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


wspr_animation_definition = Struct("animation_definition", 
    UInt32("frame"),
    SInt16("sprite_index_0"),
    SInt16("sprite_index_1"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


wspr_meta_def = BlockDef("wspr", 
    Bool32("animation_flags", 
        "loops",
        ),
    h3_reflexive("animation_definition", wspr_animation_definition),
    h3_rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )