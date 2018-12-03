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


wrot_animation_definition = Struct("animation_definition", 
    UInt32("frame"),
    SEnum16("anchor", *wscl_animation_definition_anchor),
    SInt16("unknown_0", VISIBLE=False),
    QStruct("custom_anchor", INCLUDE=xy_float),
    Float("rotation_amount"),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wrot_body = Struct("tagdata", 
    Bool32("animation_flags", 
        "loops",
        ),
    h3_reflexive("animation_definition", wrot_animation_definition),
    h3_rawdata_ref("date"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wrot_def

wrot_def = TagDef("wrot",
    h3_blam_header('wrot'),
    wrot_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wrot"], endian=">", tag_cls=H3Tag
    )