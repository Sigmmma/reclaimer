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


wacd_body = Struct("tagdata",
    h3_dependency("focus"),
    h3_dependency("unfocus"),
    h3_dependency("unknown_0"),
    h3_dependency("unknown_1"),
    h3_dependency("unknown_2"),
    h3_dependency("unknown_3"),
    h3_dependency("out"),
    h3_dependency("in"),
    h3_dependency("unknown_4"),
    h3_dependency("unknown_5"),
    h3_dependency("unknown_6"),
    h3_dependency("unknown_7"),
    h3_dependency("unknown_8"),
    h3_dependency("unknown_9"),
    h3_dependency("unknown_10"),
    h3_dependency("unknown_11"),
    h3_dependency("focus_in"),
    h3_dependency("focus_out"),
    h3_dependency("unknown_12"),
    h3_dependency("unknown_13"),
    h3_dependency("unknown_14"),
    h3_dependency("unknown_15"),
    h3_dependency("unknown_16"),
    h3_dependency("unknown_17"),
    h3_dependency("unknown_18"),
    h3_dependency("unknown_19"),
    h3_dependency("unknown_20"),
    h3_dependency("unknown_21"),
    h3_dependency("unknown_22"),
    h3_dependency("unknown_23"),
    h3_dependency("unknown_24"),
    h3_dependency("unknown_25"),
    h3_dependency("unknown_26"),
    h3_dependency("unknown_27"),
    h3_dependency("unknown_28"),
    h3_dependency("unknown_29"),
    ENDIAN=">", SIZE=576
    )


def get():
    return wacd_def

wacd_def = TagDef("wacd",
    h3_blam_header('wacd'),
    wacd_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wacd"], endian=">", tag_cls=H3Tag
    )
