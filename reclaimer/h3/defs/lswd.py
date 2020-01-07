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
# revision: 1		author: -DeToX-
# 	Mapped plugin structure a new.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


lswd_unknown_0 = Struct("unknown_0",
    BytesRaw("unknown", SIZE=60, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=60
    )


lswd_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=8, VISIBLE=False),
    h3_dependency("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=52, VISIBLE=False),
    h3_reflexive("unknown_3", lswd_unknown_0),
    ENDIAN=">", SIZE=88
    )


def get():
    return lswd_def

lswd_def = TagDef("lswd",
    h3_blam_header('lswd'),
    lswd_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["lswd"], endian=">", tag_cls=H3Tag
    )
