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
# revision: 2		author: Lord Zedd
# 	thx h2
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


mdlg_line_variant = Struct("variant",
    h3_string_id("variant_designation"),
    h3_dependency("sound"),
    h3_string_id("sound_effect"),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


mdlg_line = Struct("line",
    h3_string_id("name"),
    h3_reflexive("variants", mdlg_line_variant),
    h3_string_id("default_sound_effect"),
    ENDIAN=">", SIZE=20
    )


mdlg_body = Struct("tagdata",
    h3_reflexive("lines", mdlg_line),
    ENDIAN=">", SIZE=12
    )


def get():
    return mdlg_def

mdlg_def = TagDef("mdlg",
    h3_blam_header('mdlg'),
    mdlg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["mdlg"], endian=">", tag_cls=H3Tag
    )
