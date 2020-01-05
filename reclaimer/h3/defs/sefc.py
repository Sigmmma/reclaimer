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
# revision: 2		author: Veegie
# 	Fixed some shit
# revision: 3		author: Lord Zedd
# 	Standardizing
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


sefc_screen_effect = Struct("screen_effect",
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    h3_rawdata_ref("function_0", VISIBLE=False),
    Float("duration"),
    h3_rawdata_ref("function_1", VISIBLE=False),
    h3_rawdata_ref("function_2", VISIBLE=False),
    Float("light_intensity"),
    Pad(8),
    Float("saturation"),
    Float("color_muting"),
    Float("brightness"),
    Float("darkness"),
    Float("shadow_brightness"),
    color_rgb_float("tint"),
    color_rgb_float("tone"),
    ENDIAN=">", SIZE=132
    )


sefc_body = Struct("tagdata",
    h3_reflexive("screen_effect", sefc_screen_effect),
    ENDIAN=">", SIZE=12
    )


def get():
    return sefc_def

sefc_def = TagDef("sefc",
    h3_blam_header('sefc'),
    sefc_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["sefc"], endian=">", tag_cls=H3Tag
    )
