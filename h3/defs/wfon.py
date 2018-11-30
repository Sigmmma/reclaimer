############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Lord Zedd
# 	I wanted to see what it did, sue me. Basically done.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


wfon_animation_definition = Struct("animation_definition", 
    UInt32("frame"),
    SInt16("font_index"),
    SInt16("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


wfon_meta_def = BlockDef("wfon", 
    Bool32("animation_flags", 
        "loops",
        ),
    h3_reflexive("animation_definition", wfon_animation_definition),
    h3_rawdata_ref("data"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )