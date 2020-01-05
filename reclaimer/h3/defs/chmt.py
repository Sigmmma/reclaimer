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
# 	Created layout of plugin
# revision: 2		author: Lord Zedd
# 	Done
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


chmt_lighting_variable = Struct("lighting_variable",
    Float("lightmap_brightness_offset"),
    ENDIAN=">", SIZE=4
    )


chmt_body = Struct("tagdata",
    h3_reflexive("lighting_variables", chmt_lighting_variable),
    ENDIAN=">", SIZE=12
    )


def get():
    return chmt_def

chmt_def = TagDef("chmt",
    h3_blam_header('chmt'),
    chmt_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["chmt"], endian=">", tag_cls=H3Tag
    )
