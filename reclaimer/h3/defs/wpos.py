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


wpos_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    Float("x_position"),
    Float("y_position"),
    Float("z_position"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=28
    )


wpos_body = Struct("tagdata",
    Bool32("animation_flags",
        "loops",
        ),
    h3_reflexive("animation_definition", wpos_animation_definition),
    h3_rawdata_ref("data"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wpos_def

wpos_def = TagDef("wpos",
    h3_blam_header('wpos'),
    wpos_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wpos"], endian=">", tag_cls=H3Tag
    )
