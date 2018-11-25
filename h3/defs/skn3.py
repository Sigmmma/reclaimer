from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

skn3_bitmap_widget_blend_method = (
    "standard",
    "unknown",
    "unknown_1",
    "alpha",
    "overlay",
    "unknown_2",
    "lighter_color",
    "unknown_3",
    "unknown_4",
    "unknown_5",
    "inverted_alpha",
    "unknown_6",
    "unknown_7",
    "unknown_8",
    )


skn3_text_widget = Struct("text_widgets",
    dependency("ancestor"),
    Bool32("flags",
        ("left_alignment", 1 << 3),
        "right_alignment",
        ("all_caps", 1 << 6),
        ("wrap_at_bounds", 1 << 13),
        ),
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    dependency("animation"),
    string_id_meta("data_source_name"),
    string_id_meta("text_string"),
    string_id_meta("text_color"),
    SInt16("text_font"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=76
    )


skn3_bitmap_widget = Struct("bitmap_widgets",
    dependency("ancestor"),
    Bool32("flags",
        ("scale_to_bounds", 1 << 3),
        "replace_with_blur",
        ("replace_with_white", 1 << 10),
        "replace_with_black",
        ),
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    dependency("animation"),
    dependency("bitmap"),
    dependency("unknown_1"),
    SEnum16("blend_method", *skn3_bitmap_widget_blend_method),
    SInt16("unknown_2"),
    SInt16("sprite_index"),
    SInt16("unknown_3"),
    string_id_meta("data_source_name"),
    string_id_meta("sprite_data_source_name"),
    ENDIAN=">", SIZE=108
    )


skn3_meta_def = BlockDef("skn3",
    Pad(4),
    reflexive("text_widgets", skn3_text_widget),
    reflexive("bitmap_widgets", skn3_bitmap_widget),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )
