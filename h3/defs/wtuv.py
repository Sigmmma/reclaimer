############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
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
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


wtuv_animation_definition = Struct("animation_definition", 
    UInt32("frame"),
    QStruct("coordinate", INCLUDE=xy_float),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


wtuv_body = Struct("tagdata", 
    Bool32("animation_flags", 
        "loops",
        ),
    h3_reflexive("animation_definition", wtuv_animation_definition),
    h3_rawdata_ref("data"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wtuv_def

wtuv_def = TagDef("wtuv",
    h3_blam_header('wtuv'),
    wtuv_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wtuv"], endian=">", tag_cls=H3Tag
    )