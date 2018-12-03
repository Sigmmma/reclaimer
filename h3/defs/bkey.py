############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Updated and copypasted.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


bkey_text_widget = Struct("text_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", 
        ("left_alignment", 1 << 3),
        "right_alignment",
        ("all_caps", 1 << 6),
        ("wrap_at_bounds", 1 << 13),
        ),
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_string_id("data_source_name"),
    h3_string_id("text_string"),
    h3_string_id("text_color"),
    SInt16("text_font"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=76
    )


bkey_bitmap_widget = Struct("bitmap_widget", 
    h3_dependency("ancestor"),
    Bool32("flags", 
        ("scale_to_bounds", 1 << 3),
        "replace_with_blur",
        ("replace_with_white", 1 << 10),
        "replace_with_black",
        ),
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_dependency("bitmap"),
    h3_dependency("unknown_1"),
    SEnum16("blend_method", *bmp3_blend_method),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("sprite_index"),
    SInt16("unknown_3", VISIBLE=False),
    h3_string_id("data_source_name"),
    h3_string_id("sprite_data_source_name"),
    ENDIAN=">", SIZE=108
    )


bkey_body = Struct("tagdata", 
    Bool32("flags", *unknown_flags_32),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_dependency("strings"),
    h3_reflexive("text_widgets", bkey_text_widget),
    h3_reflexive("bitmap_widgets", bkey_bitmap_widget),
    ENDIAN=">", SIZE=84
    )


def get():
    return bkey_def

bkey_def = TagDef("bkey",
    h3_blam_header('bkey'),
    bkey_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["bkey"], endian=">", tag_cls=H3Tag
    )