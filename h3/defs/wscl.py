############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DarkShallFall
# 	X, y scale and found types for other unknowns.
# revision: 3		author: Lord Zedd
# 	Basically done.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


wscl_animation_definition = Struct("animation_definition", 
    UInt32("frame"),
    SEnum16("anchor", *wscl_animation_definition_anchor),
    SInt16("unknown_0", VISIBLE=False),
    QStruct("custom_anchor", INCLUDE=xy_float),
    Float("x_scale"),
    Float("y_scale"),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


wscl_meta_def = BlockDef("wscl", 
    Bool32("animation_flags", 
        "loops",
        ),
    h3_reflexive("animation_definition", wscl_animation_definition),
    h3_rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )