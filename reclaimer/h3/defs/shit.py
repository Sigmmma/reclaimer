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
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


shit_body = Struct("tagdata",
    h3_dependency("unknown_0"),
    h3_dependency("unknown_1"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=9, VISIBLE=False),
    color_rgb_float("color_0"),
    Float("unknown_2", VISIBLE=False),
    color_rgb_float("color_1"),
    Float("unknown_3", VISIBLE=False),
    color_rgb_float("color_2"),
    Float("unknown_4", VISIBLE=False),
    color_rgb_float("color_3"),
    Float("unknown_5", VISIBLE=False),
    color_rgb_float("color_4"),
    Float("unknown_6", VISIBLE=False),
    color_rgb_float("color_5"),
    Float("unknown_7", VISIBLE=False),
    ENDIAN=">", SIZE=164
    )


def get():
    return shit_def

shit_def = TagDef("shit",
    h3_blam_header('shit'),
    shit_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["shit"], endian=">", tag_cls=H3Tag
    )
