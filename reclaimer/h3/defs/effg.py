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
# 	Standardizing
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


effg_unknown_unknown_2 = Struct("unknown_2",
    SInt32("unknown_0"),
    SInt32("unknown_1"),
    Pad(4),
    SInt32("unknown_3"),
    ENDIAN=">", SIZE=16
    )


effg_unknown = Struct("unknown",
    SInt32("unknown_0"),
    SInt32("unknown_1"),
    h3_reflexive("unknown_2", effg_unknown_unknown_2),
    ENDIAN=">", SIZE=20
    )


effg_body = Struct("tagdata",
    h3_reflexive("unknown", effg_unknown),
    ENDIAN=">", SIZE=12
    )


def get():
    return effg_def

effg_def = TagDef("effg",
    h3_blam_header('effg'),
    effg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["effg"], endian=">", tag_cls=H3Tag
    )
