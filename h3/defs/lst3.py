from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


lst3_list_widget_item = Struct("list_widget_items",
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


lst3_meta_def = BlockDef("lst3",
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
    reflexive("list_widget_items", lst3_list_widget_item),
    dependency("up_arrow_bitmap"),
    dependency("down_arrow_bitmap"),
    TYPE=Struct, ENDIAN=">", SIZE=112
    )