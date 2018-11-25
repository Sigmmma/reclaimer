from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

ligh_type = (
    "sphere",
    "projective",
    )


ligh_meta_def = BlockDef("ligh",
    Bool32("flags",
        ("no_shadow", 1 << 1),
        "only_render_in_first_person",
        "only_render_in_third_person",
        ("snap_to_first_person_camera_req_only_first_person", 1 << 7),
        ),
    SEnum16("type", *ligh_type),
    SInt16("unknown"),
    Float("light_range"),
    Float("near_width"),
    Float("height_stretch"),
    float_rad("field_of_view"),
    string_id_meta("function_name"),
    string_id_meta("function_name_1"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    Pad(4),
    rawdata_ref("function"),
    string_id_meta("function_name_2"),
    string_id_meta("function_name_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    Pad(4),
    rawdata_ref("function_1"),
    dependency("gel_map"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    SInt8("unknown_11"),
    SInt8("unknown_12"),
    SInt8("unknown_13"),
    SInt8("unknown_14"),
    dependency("lens_flare"),
    TYPE=Struct, ENDIAN=">", SIZE=148
    )