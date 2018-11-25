from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


mdl3_camera_refinement_zoom_data_1 = Struct("zoom_data_1",
    rawdata_ref("unknown"),
    ENDIAN=">", SIZE=20
    )


mdl3_camera_refinement_zoom_data_2 = Struct("zoom_data_2",
    rawdata_ref("unknown"),
    ENDIAN=">", SIZE=20
    )


mdl3_camera_refinement = Struct("camera_refinement",
    string_id_meta("biped"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    reflexive("zoom_data_1", mdl3_camera_refinement_zoom_data_1),
    reflexive("zoom_data_2", mdl3_camera_refinement_zoom_data_2),
    ENDIAN=">", SIZE=60
    )


mdl3_meta_def = BlockDef("mdl3",
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
    reflexive("camera_refinement", mdl3_camera_refinement),
    TYPE=Struct, ENDIAN=">", SIZE=56
    )