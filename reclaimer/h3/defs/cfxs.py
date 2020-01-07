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
# 	Standardizing.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


cfxs_body = Struct("tagdata",
    Bool16("flags_0",
        "disable_brightness",
        ("disable_overexposure", 1 << 2),
        ),
    SInt16("unknown_0", VISIBLE=False),
    Float("overexposure_amount"),
    Float("overexposure_unknown_0"),
    Float("overexposure_unknown_1"),
    Float("brightness_amount"),
    Float("brightness_unknown_0"),
    Float("brightness_unknown_1"),
    Float("brightness_unknown_2"),
    Bool16("flags_1",
        "disable",
        ),
    SInt16("unknown_1", VISIBLE=False),
    Float("unknown_2"),
    Bool16("flags_2",
        "disable",
        ),
    SInt16("unknown_3", VISIBLE=False),
    Float("unknown_4"),
    Bool16("flags_3",
        "disable",
        ),
    SInt16("unknown_5", VISIBLE=False),
    Float("base_0"),
    Float("min_0"),
    Float("max_0"),
    Bool16("flags_4",
        "disable",
        ),
    SInt16("unknown_6", VISIBLE=False),
    Float("base_1"),
    Float("min_1"),
    Float("max_1"),
    Bool16("flags_5",
        "disable",
        ),
    SInt16("unknown_7", VISIBLE=False),
    Float("base_2"),
    Float("min_2"),
    Float("max_2"),
    Bool16("flags_6",
        "disable",
        ),
    SInt16("unknown_8", VISIBLE=False),
    color_rgb_float("color_0"),
    Bool16("flags_7",
        "disable",
        ),
    SInt16("unknown_9", VISIBLE=False),
    color_rgb_float("color_1"),
    Bool16("flags_8",
        "disable",
        ),
    SInt16("unknown_10", VISIBLE=False),
    color_rgb_float("color_2"),
    Bool16("flags_9",
        "disable",
        ),
    SInt16("unknown_11", VISIBLE=False),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("unknown_14"),
    Bool16("flags_10",
        "disable",
        ),
    SInt16("unknown_15", VISIBLE=False),
    Float("unknown_16"),
    Float("unknown_17"),
    Float("unknown_18"),
    Bool16("flags_11",
        "disable",
        ),
    SInt16("unknown_19", VISIBLE=False),
    Float("unknown_20"),
    Float("unknown_21"),
    Float("unknown_22"),
    SInt32("unknown_23"),
    Bool16("flags_12",
        "disable",
        ),
    SInt16("unknown_24", VISIBLE=False),
    Float("base_3"),
    Float("min_3"),
    Float("max_3"),
    Bool16("flags_13",
        "disable",
        ),
    SInt16("unknown_25", VISIBLE=False),
    Float("base_4"),
    Float("min_4"),
    Float("max_4"),
    ENDIAN=">", SIZE=228
    )


def get():
    return cfxs_def

cfxs_def = TagDef("cfxs",
    h3_blam_header('cfxs'),
    cfxs_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["cfxs"], endian=">", tag_cls=H3Tag
    )
