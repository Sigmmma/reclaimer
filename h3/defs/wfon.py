############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Lord Zedd
# 	I wanted to see what it did, sue me. Basically done.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


wfon_animation_definition = Struct("animation_definition", 
    UInt32("frame"),
    SInt16("font_index"),
    SInt16("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


wfon_body = Struct("tagdata", 
    Bool32("animation_flags", 
        "loops",
        ),
    h3_reflexive("animation_definition", wfon_animation_definition),
    h3_rawdata_ref("data"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wfon_def

wfon_def = TagDef("wfon",
    h3_blam_header('wfon'),
    wfon_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wfon"], endian=">", tag_cls=H3Tag
    )