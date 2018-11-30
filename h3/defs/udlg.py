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


udlg_vocalization = Struct("vocalization", 
    Bool16("flags", 
        "new_vocalization",
        ),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("vocalization"),
    h3_dependency("sound"),
    ENDIAN=">", SIZE=24
    )


udlg_meta_def = BlockDef("udlg", 
    h3_dependency("global_dialogue_info"),
    Bool32("flags", 
        "female",
        ),
    h3_reflexive("vocalizations", udlg_vocalization),
    h3_string_id("mission_dialogue_designator"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )