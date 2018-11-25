from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

pmdf_meshe_index_buffer_type = (
    "point_list",
    "line_list",
    "line_strip",
    "triange_list",
    "triange_fan",
    "triange_strip",
    )

pmdf_meshe_prt_type = (
    "none",
    "ambient",
    "linear",
    "quadratic",
    )

pmdf_meshe_vertex_type = (
    "world",
    "rigid",
    "skinned",
    "particle_model",
    "flat_world",
    "flat_rigid",
    "flat_skinned",
    "screen",
    "debug",
    "transparent",
    "particle",
    "contrail",
    "light_volume",
    "chud_simple",
    "chud_fancy",
    "decorator",
    "tiny_position",
    "patchy_fog",
    "water",
    "ripple",
    "implicit",
    "beam",
    )


pmdf_meshe_part = Struct("parts",
    SInt16("material_index"),
    SInt16("unknown_nodey_index"),
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("subpart_index"),
    SInt16("subpart_count"),
    SInt8("unknown_enum"),
    Bool8("flags",
        ("water", 1 << 3),
        ),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=16
    )


pmdf_meshe_subpart = Struct("subparts",
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


pmdf_meshe_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_contents",
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


pmdf_meshe_instanced_geometry_indice = Struct("instanced_geometry_indices",
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    reflexive("instanced_geometry_mesh_contents", pmdf_meshe_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


pmdf_meshe_unknown_water = Struct("unknown_water",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


pmdf_meshe = Struct("meshes",
    reflexive("parts", pmdf_meshe_part),
    reflexive("subparts", pmdf_meshe_subpart),
    SInt16("vertex_buffer_index_1"),
    SInt16("vertex_buffer_index_2"),
    SInt16("vertex_buffer_index_3"),
    SInt16("vertex_buffer_index_4"),
    SInt16("vertex_buffer_index_5"),
    SInt16("vertex_buffer_index_6"),
    SInt16("vertex_buffer_index_7"),
    SInt16("vertex_buffer_index_8"),
    SInt16("index_buffer_index_1"),
    SInt16("index_buffer_index_2"),
    Bool8("flags",
        "has_vertex_colors",
        ),
    SInt8("rigid_node"),
    SEnum8("vertex_type", *pmdf_meshe_vertex_type),
    SEnum8("prt_type", *pmdf_meshe_prt_type),
    SEnum8("index_buffer_type", *pmdf_meshe_index_buffer_type),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    reflexive("instanced_geometry_indices", pmdf_meshe_instanced_geometry_indice),
    reflexive("unknown_water", pmdf_meshe_unknown_water),
    ENDIAN=">", SIZE=76
    )


pmdf_compression_info = Struct("compression_info",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("position_bounds_x_min"),
    Float("position_bounds_x_max"),
    Float("position_bounds_y_min"),
    Float("position_bounds_y_max"),
    Float("position_bounds_z_min"),
    Float("position_bounds_z_max"),
    Float("texcoord_bounds_x_min"),
    Float("texcoord_bounds_x_max"),
    Float("texcoord_bounds_y_min"),
    Float("texcoord_bounds_y_max"),
    ENDIAN=">", SIZE=44
    )


pmdf_unknown_nodey = Struct("unknown_nodey",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    SInt8("node_index"),
    SInt8("node_index_1"),
    SInt8("node_index_2"),
    SInt8("node_index_3"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    ENDIAN=">", SIZE=48
    )


pmdf_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    SInt16("unknown_1"),
    rawdata_ref("unknown_2"),
    ENDIAN=">", SIZE=24
    )


pmdf_unknown_meshe_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


pmdf_unknown_meshe = Struct("unknown_meshes",
    rawdata_ref("unknown"),
    reflexive("unknown_1", pmdf_unknown_meshe_unknown_1),
    ENDIAN=">", SIZE=32
    )


pmdf_node_map_unknown = Struct("unknown",
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


pmdf_node_map = Struct("node_maps",
    reflexive("unknown", pmdf_node_map_unknown),
    ENDIAN=">", SIZE=12
    )


pmdf_unknown_3_unknown = Struct("unknown",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


pmdf_unknown_3 = Struct("unknown_3",
    reflexive("unknown", pmdf_unknown_3_unknown),
    ENDIAN=">", SIZE=12
    )


pmdf_unknown_yo = Struct("unknown_yo",
    Pad(12),
    SInt16("unknown_index"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=16
    )


pmdf_unknown_5 = Struct("unknown_5",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


pmdf_meta_def = BlockDef("pmdf",
    SInt32("unknown"),
    reflexive("meshes", pmdf_meshe),
    reflexive("compression_info", pmdf_compression_info),
    reflexive("unknown_nodey", pmdf_unknown_nodey),
    reflexive("unknown_1", pmdf_unknown_1),
    Pad(12),
    reflexive("unknown_meshes", pmdf_unknown_meshe),
    reflexive("node_maps", pmdf_node_map),
    reflexive("unknown_3", pmdf_unknown_3),
    Pad(12),
    reflexive("unknown_yo", pmdf_unknown_yo),
    UInt16("zone_asset_salt"),
    UInt16("zone_asset_index"),
    SInt32("useless_padding"),
    reflexive("unknown_5", pmdf_unknown_5),
    TYPE=Struct, ENDIAN=">", SIZE=144
    )