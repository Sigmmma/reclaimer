from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

mode_meshe_index_buffer_type = (
    "point_list",
    "line_list",
    "line_strip",
    "triange_list",
    "triange_fan",
    "triange_strip",
    )

mode_meshe_prt_type = (
    "none",
    "ambient",
    "linear",
    "quadratic",
    )

mode_meshe_vertex_type = (
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


mode_region_permutation = Struct("permutations",
    string_id_meta("name"),
    SInt16("mesh_index"),
    SInt16("mesh_count"),
    SInt32("unknown"),
    SInt32("unknown_1"),
    ENDIAN=">", SIZE=16
    )


mode_region = Struct("regions",
    string_id_meta("name"),
    reflexive("permutations", mode_region_permutation),
    ENDIAN=">", SIZE=16
    )


mode_instance = Struct("instances",
    string_id_meta("name"),
    SInt32("node_index"),
    Float("default_scale"),
    Float("inverse_forward_i"),
    Float("inverse_forward_j"),
    Float("inverse_forward_k"),
    Float("inverse_left_i"),
    Float("inverse_left_j"),
    Float("inverse_left_k"),
    Float("inverse_up_i"),
    Float("inverse_up_j"),
    Float("inverse_up_k"),
    Float("inverse_position_x"),
    Float("inverse_position_y"),
    Float("inverse_position_z"),
    ENDIAN=">", SIZE=60
    )


mode_node = Struct("nodes",
    string_id_meta("name"),
    SInt16("parent_node"),
    SInt16("first_child_node"),
    SInt16("next_sibling_node"),
    SInt16("import_node_index"),
    Float("default_translation_x"),
    Float("default_translation_y"),
    Float("default_translation_z"),
    Float("default_rotation_i"),
    Float("default_rotation_j"),
    Float("default_rotation_k"),
    Float("default_rotation_w"),
    Float("default_scale"),
    Float("inverse_forward_i"),
    Float("inverse_forward_j"),
    Float("inverse_forward_k"),
    Float("inverse_left_i"),
    Float("inverse_left_j"),
    Float("inverse_left_k"),
    Float("inverse_up_i"),
    Float("inverse_up_j"),
    Float("inverse_up_k"),
    Float("inverse_position_x"),
    Float("inverse_position_y"),
    Float("inverse_position_z"),
    Float("distance_from_parent"),
    ENDIAN=">", SIZE=96
    )


mode_marker_group_marker = Struct("markers",
    SInt8("region_index"),
    SInt8("permutation_index"),
    SInt8("node_index"),
    SInt8("unknown"),
    Float("translation_x"),
    Float("translation_y"),
    Float("translation_z"),
    Float("rotation_i"),
    Float("rotation_j"),
    Float("rotation_k"),
    Float("rotation_w"),
    Float("scale"),
    ENDIAN=">", SIZE=36
    )


mode_marker_group = Struct("marker_groups",
    string_id_meta("name"),
    reflexive("markers", mode_marker_group_marker),
    ENDIAN=">", SIZE=16
    )


mode_material_propertie = Struct("properties",
    SInt16("type"),
    SInt16("int_value"),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    Float("real_value"),
    ENDIAN=">", SIZE=12
    )


mode_material = Struct("materials",
    dependency("shader"),
    reflexive("properties", mode_material_propertie),
    SInt32("unknown"),
    SInt8("breakable_surface_index"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    ENDIAN=">", SIZE=36
    )


mode_meshe_part = Struct("parts",
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


mode_meshe_subpart = Struct("subparts",
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


mode_meshe_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_contents",
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


mode_meshe_instanced_geometry_indice = Struct("instanced_geometry_indices",
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    reflexive("instanced_geometry_mesh_contents", mode_meshe_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


mode_meshe_unknown_water = Struct("unknown_water",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


mode_meshe = Struct("meshes",
    reflexive("parts", mode_meshe_part),
    reflexive("subparts", mode_meshe_subpart),
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
    SEnum8("vertex_type", *mode_meshe_vertex_type),
    SEnum8("prt_type", *mode_meshe_prt_type),
    SEnum8("index_buffer_type", *mode_meshe_index_buffer_type),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    reflexive("instanced_geometry_indices", mode_meshe_instanced_geometry_indice),
    reflexive("unknown_water", mode_meshe_unknown_water),
    ENDIAN=">", SIZE=76
    )


mode_compression_info = Struct("compression_info",
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


mode_unknown_nodey = Struct("unknown_nodey",
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


mode_unknown_5 = Struct("unknown_5",
    SInt16("unknown"),
    SInt16("unknown_1"),
    rawdata_ref("unknown_2"),
    ENDIAN=">", SIZE=24
    )


mode_unknown_meshe_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


mode_unknown_meshe = Struct("unknown_meshes",
    rawdata_ref("unknown"),
    reflexive("unknown_1", mode_unknown_meshe_unknown_1),
    ENDIAN=">", SIZE=32
    )


mode_node_map_unknown = Struct("unknown",
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


mode_node_map = Struct("node_maps",
    reflexive("unknown", mode_node_map_unknown),
    ENDIAN=">", SIZE=12
    )


mode_unknown_7_unknown = Struct("unknown",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


mode_unknown_7 = Struct("unknown_7",
    reflexive("unknown", mode_unknown_7_unknown),
    ENDIAN=">", SIZE=12
    )


mode_unknown_yo = Struct("unknown_yo",
    Pad(12),
    SInt16("unknown_index"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=16
    )


mode_unknown_9 = Struct("unknown_9",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    ENDIAN=">", SIZE=28
    )


mode_unknown_10 = Struct("unknown_10",
    Pad(336),
    ENDIAN=">", SIZE=336
    )


mode_runtime_node = Struct("runtime_nodes",
    Float("default_rotation_i"),
    Float("default_rotation_j"),
    Float("default_rotation_k"),
    Float("default_rotation_w"),
    Float("default_translation_x"),
    Float("default_translation_y"),
    Float("default_translation_z"),
    Float("default_scale"),
    ENDIAN=">", SIZE=32
    )


mode_meta_def = BlockDef("mode",
    string_id_meta("name"),
    Bool16("flags",
        ("force_node_maps", 1 << 2),
        ),
    SInt16("unknown"),
    SInt32("model_checksum"),
    reflexive("regions", mode_region),
    Pad(4),
    SInt32("instance_starting_mesh_index"),
    reflexive("instances", mode_instance),
    Pad(4),
    reflexive("nodes", mode_node),
    reflexive("marker_groups", mode_marker_group),
    reflexive("materials", mode_material),
    Pad(16),
    SInt32("unknown_4"),
    reflexive("meshes", mode_meshe),
    reflexive("compression_info", mode_compression_info),
    reflexive("unknown_nodey", mode_unknown_nodey),
    reflexive("unknown_5", mode_unknown_5),
    Pad(12),
    reflexive("unknown_meshes", mode_unknown_meshe),
    reflexive("node_maps", mode_node_map),
    reflexive("unknown_7", mode_unknown_7),
    Pad(12),
    reflexive("unknown_yo", mode_unknown_yo),
    UInt16("zone_asset_salt"),
    UInt16("zone_asset_index"),
    SInt32("useless_padding"),
    reflexive("unknown_9", mode_unknown_9),
    Pad(192),
    reflexive("unknown_10", mode_unknown_10),
    reflexive("runtime_nodes", mode_runtime_node),
    TYPE=Struct, ENDIAN=">", SIZE=460
    )