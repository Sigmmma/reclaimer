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
# revision: 2		author: Deadcanadian
# 	naming stuff
# revision: 3		author: OrangeMohawk
# 	Data types
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


dsrc_data_integer_value = Struct("integer_value",
    h3_string_id("data_type"),
    SInt32("value"),
    ENDIAN=">", SIZE=8
    )


dsrc_data_string_value = Struct("string_value",
    h3_string_id("data_type"),
    StrLatin1("value", SIZE=20),
    ENDIAN=">", SIZE=36
    )


dsrc_data_stringid_value = Struct("stringid_value",
    h3_string_id("data_type"),
    h3_string_id("value"),
    ENDIAN=">", SIZE=8
    )


dsrc_data = Struct("data",
    h3_reflexive("integer_values", dsrc_data_integer_value),
    h3_reflexive("string_values", dsrc_data_string_value),
    h3_reflexive("stringid_values", dsrc_data_stringid_value),
    h3_string_id("unknown"),
    ENDIAN=">", SIZE=40
    )


dsrc_body = Struct("tagdata",
    h3_string_id("name"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    h3_reflexive("data", dsrc_data),
    ENDIAN=">", SIZE=28
    )


def get():
    return dsrc_def

dsrc_def = TagDef("dsrc",
    h3_blam_header('dsrc'),
    dsrc_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["dsrc"], endian=">", tag_cls=H3Tag
    )
