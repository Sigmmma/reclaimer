from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


txt3_meta_def = BlockDef("txt3",
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
    TYPE=Struct, ENDIAN=">", SIZE=60
    )