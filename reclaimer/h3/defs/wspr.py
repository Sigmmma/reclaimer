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


wspr_animation_definition = Struct("animation_definition",
    UInt32("frame"),
    SInt16("sprite_index_0"),
    SInt16("sprite_index_1"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


wspr_body = Struct("tagdata",
    Bool32("animation_flags",
        "loops",
        ),
    h3_reflexive("animation_definition", wspr_animation_definition),
    h3_rawdata_ref("data"),
    ENDIAN=">", SIZE=36
    )


def get():
    return wspr_def

wspr_def = TagDef("wspr",
    h3_blam_header('wspr'),
    wspr_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wspr"], endian=">", tag_cls=H3Tag
    )
