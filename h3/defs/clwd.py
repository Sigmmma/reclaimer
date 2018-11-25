from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

clwd_integration_type = (
    "verlet",
    )


clwd_vertice = Struct("vertices",
    Float("initial_position_x"),
    Float("initial_position_y"),
    Float("initial_position_z"),
    Float("uv_i"),
    Float("uv_j"),
    ENDIAN=">", SIZE=20
    )


clwd_indice = Struct("indices",
    SInt16("idx"),
    ENDIAN=">", SIZE=2
    )


clwd_link = Struct("links",
    SInt16("index_1"),
    SInt16("index_2"),
    Float("default_distance"),
    ENDIAN=">", SIZE=8
    )


clwd_meta_def = BlockDef("clwd",
    Bool32("flags",
        "doesn_t_use_wind",
        "uses_grid_attach_top",
        ),
    string_id_meta("marker_attachment_name"),
    string_id_meta("second_marker_attachment_name"),
    dependency("shader"),
    SInt16("grid_x_dimension"),
    SInt16("grid_y_dimension"),
    Float("grid_spacing_x"),
    Float("grid_spacing_y"),
    Pad(12),
    SEnum16("integration_type", *clwd_integration_type),
    SInt16("number_iterations"),
    Float("weight"),
    Float("drag"),
    Float("wind_scale"),
    Float("wind_flappiness_scale"),
    Float("longest_rod"),
    Pad(24),
    reflexive("vertices", clwd_vertice),
    reflexive("indices", clwd_indice),
    Pad(12),
    reflexive("links", clwd_link),
    TYPE=Struct, ENDIAN=">", SIZE=148
    )