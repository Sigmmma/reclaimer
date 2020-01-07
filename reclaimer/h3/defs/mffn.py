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


mffn_location = Struct("location",
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


mffn_unknown_2 = Struct("unknown_2",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    Float("unknown_4", VISIBLE=False),
    Float("unknown_5", VISIBLE=False),
    h3_rawdata_ref("unknown_6"),
    Float("unknown_7", VISIBLE=False),
    h3_rawdata_ref("unknown_8"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    h3_dependency("effect"),
    ENDIAN=">", SIZE=112
    )


mffn_body = Struct("tagdata",
    h3_dependency("render_model"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    h3_reflexive("locations", mffn_location),
    h3_reflexive("unknown_2", mffn_unknown_2),
    ENDIAN=">", SIZE=56
    )


def get():
    return mffn_def

mffn_def = TagDef("mffn",
    h3_blam_header('mffn'),
    mffn_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["mffn"], endian=">", tag_cls=H3Tag
    )
