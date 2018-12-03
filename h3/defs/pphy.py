############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	H2 Port
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


pphy_body = Struct("tagdata", 
    Bool32("flags", *unknown_flags_32),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=16, VISIBLE=False),
    Float("density", VISIBLE=False),
    Float("air_friction"),
    Float("water_friction"),
    Float("surface_friction"),
    Float("elasticity"),
    BytesRaw("unknown_4", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


def get():
    return pphy_def

pphy_def = TagDef("pphy",
    h3_blam_header('pphy'),
    pphy_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["pphy"], endian=">", tag_cls=H3Tag
    )