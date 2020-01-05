#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
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
from .objs.tag import *
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


wscl_body = Struct("tagdata",
    Bool32("animation_flags",
        "loops",
        ),
    h3_reflexive("animation_definition", wscl_animation_definition),
    h3_rawdata_ref("data"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wscl_def

wscl_def = TagDef("wscl",
    h3_blam_header('wscl'),
    wscl_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wscl"], endian=">", tag_cls=H3Tag
    )
