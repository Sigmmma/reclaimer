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
# revision: 2		author: DeadCanadian
# 	named a few things
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


jmrq_sandbox_text_value_pair_text_value_pair = Struct("text_value_pair",
    Bool8("flags",
        "default",
        "unchanged",
        "_2",
        "_3",
        ),
    SEnum8("expected_value_type", *sily_text_value_pair_expected_value_type),
    SInt16("unknown", VISIBLE=False),
    SInt32("int_value"),
    h3_string_id("ref_name"),
    h3_string_id("name"),
    h3_string_id("description"),
    ENDIAN=">", SIZE=20
    )


jmrq_sandbox_text_value_pair = Struct("sandbox_text_value_pair",
    h3_string_id("parameter_name"),
    h3_reflexive("text_value_pairs", jmrq_sandbox_text_value_pair_text_value_pair),
    ENDIAN=">", SIZE=16
    )


jmrq_body = Struct("tagdata",
    h3_reflexive("sandbox_text_value_pairs", jmrq_sandbox_text_value_pair),
    ENDIAN=">", SIZE=12
    )


def get():
    return jmrq_def

jmrq_def = TagDef("jmrq",
    h3_blam_header('jmrq'),
    jmrq_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["jmrq"], endian=">", tag_cls=H3Tag
    )
