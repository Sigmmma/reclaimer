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
# 	Woo
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


sgp__body = Struct("tagdata",
    h3_dependency("underwater_environment"),
    h3_dependency("underwater_loop"),
    BytesRaw("unknown", SIZE=8, VISIBLE=False),
    h3_dependency("enter_underater"),
    h3_dependency("exit_underwater"),
    ENDIAN=">", SIZE=72
    )


def get():
    return sgp__def

sgp__def = TagDef("sgp!",
    h3_blam_header('sgp!'),
    sgp__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["sgp!"], endian=">", tag_cls=H3Tag
    )
