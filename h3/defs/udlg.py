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


udlg_vocalization = Struct("vocalization", 
    Bool16("flags", 
        "new_vocalization",
        ),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("vocalization"),
    h3_dependency("sound"),
    ENDIAN=">", SIZE=24
    )


udlg_body = Struct("tagdata", 
    h3_dependency("global_dialogue_info"),
    Bool32("flags", 
        "female",
        ),
    h3_reflexive("vocalizations", udlg_vocalization),
    h3_string_id("mission_dialogue_designator"),
    ENDIAN=">", SIZE=36
    )


def get():
    return udlg_def

udlg_def = TagDef("udlg",
    h3_blam_header('udlg'),
    udlg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["udlg"], endian=">", tag_cls=H3Tag
    )