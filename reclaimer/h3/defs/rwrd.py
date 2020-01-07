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


rwrd_body = Struct("tagdata",
    BytesRaw("unknown", SIZE=76, VISIBLE=False),
    ENDIAN=">", SIZE=76
    )


def get():
    return rwrd_def

rwrd_def = TagDef("rwrd",
    h3_blam_header('rwrd'),
    rwrd_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["rwrd"], endian=">", tag_cls=H3Tag
    )
