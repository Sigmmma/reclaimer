############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
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


lst3_meta_def = BlockDef("lst3", 
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
    TYPE=Struct, ENDIAN=">", SIZE=112
    )