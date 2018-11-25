from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

grup_bitmap_widget_blend_method = (
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


grup_list_widget_list_widget_item = Struct("list_widget_items",
    Bool32("flags",
        ),
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    dependency("animation"),
    string_id_meta("target"),
    ENDIAN=">", SIZE=48
    )


grup_list_widget = Struct("list_widgets",
    dependency("ancestor"),
    Bool32("flags",
        ("horizontal", 1 << 4),
        "loops",
        ),
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    dependency("animation"),
    string_id_meta("data_source_name"),
    dependency("skin"),
    SInt32("row_count"),
    reflexive("list_widget_items", grup_list_widget_list_widget_item),
    dependency("up_arrow_bitmap"),
    dependency("down_arrow_bitmap"),
    ENDIAN=">", SIZE=128
    )


grup_text_widget = Struct("text_widgets",
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


grup_bitmap_widget = Struct("bitmap_widgets",
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
    SEnum16("blend_method", *grup_bitmap_widget_blend_method),
    SInt16("unknown_2"),
    SInt16("sprite_index"),
    SInt16("unknown_3"),
    string_id_meta("data_source_name"),
    string_id_meta("sprite_data_source_name"),
    ENDIAN=">", SIZE=108
    )


grup_model_widget_camera_refinement_zoom_data_1 = Struct("zoom_data_1",
    rawdata_ref("unknown"),
    ENDIAN=">", SIZE=20
    )


grup_model_widget_camera_refinement_zoom_data_2 = Struct("zoom_data_2",
    rawdata_ref("unknown"),
    ENDIAN=">", SIZE=20
    )


grup_model_widget_camera_refinement = Struct("camera_refinement",
    string_id_meta("biped"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    reflexive("zoom_data_1", grup_model_widget_camera_refinement_zoom_data_1),
    reflexive("zoom_data_2", grup_model_widget_camera_refinement_zoom_data_2),
    ENDIAN=">", SIZE=60
    )


grup_model_widget = Struct("model_widgets",
    dependency("ancestor"),
    Bool32("flags",
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
    reflexive("camera_refinement", grup_model_widget_camera_refinement),
    ENDIAN=">", SIZE=72
    )


grup_meta_def = BlockDef("grup",
    Bool32("flags",
        ("initially_hidden", 1 << 3),
        ),
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("layer"),
    SInt16("widescreen_y_offset"),
    SInt16("widescreen_x_offset"),
    SInt16("widescreen_y_unknown"),
    SInt16("widescreen_x_unknown"),
    SInt16("standard_y_offset"),
    SInt16("standard_x_offset"),
    SInt16("standard_y_unknown"),
    SInt16("standard_x_unknown"),
    dependency("animation"),
    reflexive("list_widgets", grup_list_widget),
    reflexive("text_widgets", grup_text_widget),
    reflexive("bitmap_widgets", grup_bitmap_widget),
    reflexive("model_widgets", grup_model_widget),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )
