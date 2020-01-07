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
# revision: 2		author: Lord Zedd
# 	Basically done.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


wclr_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    color_argb_float("color"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wclr_body = Struct("tagdata",
    Bool32("animation_flags",
        "loops",
        ),
    h3_reflexive("animation_definition", wclr_animation_definition),
    h3_rawdata_ref("data"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wclr_def

wclr_def = TagDef("wclr",
    h3_blam_header('wclr'),
    wclr_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wclr"], endian=">", tag_cls=H3Tag
    )
