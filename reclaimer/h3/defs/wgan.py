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
# 	Idents labled.
# revision: 3		author: Lord Zedd
# 	Basically done.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


wgan_body = Struct("tagdata",
    h3_string_id("unknown_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_dependency("widget_color"),
    h3_dependency("widget_position"),
    h3_dependency("widget_rotation"),
    h3_dependency("widget_scale"),
    h3_dependency("widget_texture_coordinate"),
    h3_dependency("widget_sprite"),
    h3_dependency("widget_font"),
    ENDIAN=">", SIZE=120
    )


def get():
    return wgan_def

wgan_def = TagDef("wgan",
    h3_blam_header('wgan'),
    wgan_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wgan"], endian=">", tag_cls=H3Tag
    )
