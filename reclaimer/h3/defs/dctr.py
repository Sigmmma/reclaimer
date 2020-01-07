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
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


dctr_body = Struct("tagdata",
    h3_dependency("model"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    h3_dependency("texture"),
    SInt16("affects_visibility"),
    SInt16("unknown_2"),
    color_rgb_float("color"),
    BytesRaw("unknown_3", SIZE=20, VISIBLE=False),
    Float("brightness_base"),
    Float("brightness_shadow"),
    BytesRaw("unknown_4", SIZE=36, VISIBLE=False),
    ENDIAN=">", SIZE=128
    )


def get():
    return dctr_def

dctr_def = TagDef("dctr",
    h3_blam_header('dctr'),
    dctr_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["dctr"], endian=">", tag_cls=H3Tag
    )
