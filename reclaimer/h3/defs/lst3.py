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
# 	named some tags
# revision: 3		author: Lord Zedd
# 	Updated and copypasted.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


lst3_list_widget_item = Struct("list_widget_item",
    Bool32("flags", *unknown_flags_32),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    h3_dependency("animation"),
    h3_string_id("target"),
    ENDIAN=">", SIZE=48
    )


lst3_body = Struct("tagdata",
    Bool32("flags",
        ("horizontal", 1 << 4),
        "loops",
        ),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    h3_dependency("animation"),
    h3_string_id("data_source_name"),
    h3_dependency("skin"),
    SInt32("row_count"),
    h3_reflexive("list_widget_items", lst3_list_widget_item),
    h3_dependency("up_arrow_bitmap"),
    h3_dependency("down_arrow_bitmap"),
    ENDIAN=">", SIZE=112
    )


def get():
    return lst3_def

lst3_def = TagDef("lst3",
    h3_blam_header('lst3'),
    lst3_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["lst3"], endian=">", tag_cls=H3Tag
    )
