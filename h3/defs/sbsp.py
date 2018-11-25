from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

sbsp_meshe_index_buffer_type = (
    "point_list",
    "line_list",
    "line_strip",
    "triange_list",
    "triange_fan",
    "triange_strip",
    )

sbsp_meshe_prt_type = (
    "none",
    "ambient",
    "linear",
    "quadratic",
    )

sbsp_meshe_vertex_type = (
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


sbsp_structure_seam_unknown_4 = Struct("unknown_4",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


sbsp_structure_seam_seam_cluster = Struct("seam_clusters",
    SInt32("cluster_index"),
    Float("centroid_x"),
    Float("centroid_y"),
    Float("centroid_z"),
    ENDIAN=">", SIZE=16
    )


sbsp_structure_seam = Struct("structure_seams",
    UInt32("unknown"),
    UInt32("unknown_1"),
    UInt32("unknown_2"),
    UInt32("unknown_3"),
    reflexive("unknown_4", sbsp_structure_seam_unknown_4),
    reflexive("seam_clusters", sbsp_structure_seam_seam_cluster),
    ENDIAN=">", SIZE=40
    )


sbsp_unknown_raw_7th = Struct("unknown_raw_7th",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


sbsp_collision_material = Struct("collision_materials",
    dependency("shader"),
    SInt16("global_material_index"),
    SInt16("conveyor_surface_index"),
    SInt16("seam_index"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=24
    )


sbsp_unknown_raw_3rd = Struct("unknown_raw_3rd",
    SInt8("unknown"),
    ENDIAN=">", SIZE=1
    )


sbsp_unknown_raw_6th = Struct("unknown_raw_6th",
    SInt16("unknown_1_start_index"),
    SInt16("unknown_1_entry_count"),
    ENDIAN=">", SIZE=4
    )


sbsp_unknown_1 = Struct("unknown_1",
    UInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


sbsp_cluster_portal_vertice = Struct("vertices",
    Float("x"),
    Float("y"),
    Float("z"),
    ENDIAN=">", SIZE=12
    )


sbsp_cluster_portal = Struct("portals",
    SInt16("portal_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_2 = Struct("unknown_2",
    Pad(120),
    ENDIAN=">", SIZE=120
    )


sbsp_fog = Struct("fog",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=8
    )


sbsp_camera_effect = Struct("camera_effects",
    string_id_meta("name"),
    dependency("effect"),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    Pad(4),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Pad(8),
    ENDIAN=">", SIZE=48
    )


sbsp_detail_object_unknown_1_unknown = Struct("unknown",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


sbsp_detail_object_unknown_1 = Struct("unknown_1",
    reflexive("unknown", sbsp_detail_object_unknown_1_unknown),
    rawdata_ref("unknown_1"),
    ENDIAN=">", SIZE=32
    )


sbsp_detail_object = Struct("detail_objects",
    Pad(28),
    reflexive("unknown_1", sbsp_detail_object_unknown_1),
    Pad(12),
    ENDIAN=">", SIZE=52
    )


sbsp_cluster_collision_mopp_code_data = Struct("data",
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sbsp_cluster_collision_mopp_code = Struct("collision_mopp_codes",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    Pad(4),
    Float("offset_x"),
    Float("offset_y"),
    Float("offset_z"),
    Float("offset_scale"),
    Pad(4),
    SInt32("data_size"),
    UInt32("data_capacity"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    reflexive("data", sbsp_cluster_collision_mopp_code_data),
    Pad(4),
    ENDIAN=">", SIZE=64
    )


sbsp_cluster_seam = Struct("seams",
    SInt8("seam_index"),
    ENDIAN=">", SIZE=1
    )


sbsp_cluster_decorator_grid = Struct("decorator_grids",
    SInt16("amount"),
    SInt8("decorator_index"),
    SInt8("decorator_index_scattering"),
    SInt32("unknown"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    Float("radius"),
    Float("grid_size_x"),
    Float("grid_size_y"),
    Float("grid_size_z"),
    Float("bounding_sphere_x"),
    Float("bounding_sphere_y"),
    Float("bounding_sphere_z"),
    ENDIAN=">", SIZE=48
    )


sbsp_cluster_unknown_16 = Struct("unknown_16",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


sbsp_cluster_unknown_17 = Struct("unknown_17",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=16
    )


sbsp_cluster = Struct("clusters",
    Float("bounds_x_min"),
    Float("bounds_x_max"),
    Float("bounds_y_min"),
    Float("bounds_y_max"),
    Float("bounds_z_min"),
    Float("bounds_z_max"),
    SInt8("unknown"),
    SInt8("scenario_sky_index"),
    SInt8("camera_effect_index"),
    SInt8("unknown_1"),
    SInt16("background_sound_environment_index"),
    SInt16("sound_clusters_a_index"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    SInt16("runtime_decal_start_index"),
    SInt16("runtime_decal_entry_count"),
    SInt16("flags"),
    Pad(12),
    reflexive("portals", sbsp_cluster_portal),
    SInt32("unknown_8"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_9"),
    Pad(8),
    dependency("bsp"),
    SInt32("cluster_index"),
    SInt32("unknown_11"),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_12"),
    Pad(12),
    reflexive("collision_mopp_codes", sbsp_cluster_collision_mopp_code),
    SInt16("mesh_index"),
    SInt16("unknown_14"),
    reflexive("seams", sbsp_cluster_seam),
    reflexive("decorator_grids", sbsp_cluster_decorator_grid),
    Pad(12),
    reflexive("unknown_16", sbsp_cluster_unknown_16),
    reflexive("unknown_17", sbsp_cluster_unknown_17),
    ENDIAN=">", SIZE=220
    )


sbsp_material_propertie = Struct("properties",
    SInt16("type"),
    SInt16("int_value"),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    Float("real_value"),
    ENDIAN=">", SIZE=12
    )


sbsp_material = Struct("materials",
    dependency("shader"),
    reflexive("properties", sbsp_material_propertie),
    SInt32("unknown"),
    SInt8("breakable_surface_index"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    ENDIAN=">", SIZE=36
    )


sbsp_sky_owner_cluster = Struct("sky_owner_cluster",
    SInt16("cluster_owner"),
    ENDIAN=">", SIZE=2
    )


sbsp_conveyor_surface = Struct("conveyor_surfaces",
    Pad(24),
    ENDIAN=">", SIZE=24
    )


sbsp_breakable_surface = Struct("breakable_surfaces",
    Pad(32),
    ENDIAN=">", SIZE=32
    )


sbsp_pathfinding_data_sector = Struct("sectors",
    Bool16("pathfinding_sector_flags",
        "sector_walkable",
        ("sector_bsp_source", 1 << 3),
        "floor",
        ),
    SInt16("hint_index"),
    SInt32("first_link"),
    ENDIAN=">", SIZE=8
    )


sbsp_pathfinding_data_link = Struct("links",
    SInt16("vertex_1"),
    SInt16("vertex_2"),
    Bool16("link_flags",
        ),
    SInt16("hint_index"),
    SInt16("forward_link"),
    SInt16("reverse_link"),
    SInt16("left_sector"),
    SInt16("right_sector"),
    ENDIAN=">", SIZE=16
    )


sbsp_pathfinding_data_ref = Struct("refs",
    SInt32("node_or_sector_ref"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_bsp_2d_node = Struct("bsp_2d_nodes",
    Pad(12),
    SInt32("left_child"),
    SInt32("right_child"),
    ENDIAN=">", SIZE=20
    )


sbsp_pathfinding_data_vertice = Struct("vertices",
    Pad(12),
    ENDIAN=">", SIZE=12
    )


sbsp_pathfinding_data_object_ref_unknown_1_unknown_1 = Struct("unknown_1",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_object_ref_unknown_1 = Struct("unknown_1",
    Pad(8),
    reflexive("unknown_1", sbsp_pathfinding_data_object_ref_unknown_1_unknown_1),
    SInt32("unknown_2"),
    ENDIAN=">", SIZE=24
    )


sbsp_pathfinding_data_object_ref = Struct("object_refs",
    Pad(4),
    reflexive("unknown_1", sbsp_pathfinding_data_object_ref_unknown_1),
    SInt32("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=24
    )


sbsp_pathfinding_data_pathfinding_hint = Struct("pathfinding_hints",
    SInt16("next_hint_index"),
    Pad(2),
    SInt16("hint_data_0"),
    SInt16("hint_data_1"),
    SInt16("hint_data_2"),
    SInt16("hint_data_3"),
    SInt16("hint_data_4"),
    SInt16("hint_data_5"),
    SInt16("hint_data_6"),
    SInt16("hint_data_7"),
    ENDIAN=">", SIZE=20
    )


sbsp_pathfinding_data_instanced_geometry_ref = Struct("instanced_geometry_refs",
    SInt16("pathfinding_object_index"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_1 = Struct("unknown_1",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_2_unknown = Struct("unknown",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_2 = Struct("unknown_2",
    reflexive("unknown", sbsp_pathfinding_data_unknown_2_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_pathfinding_data_unknown_3_unknown_3 = Struct("unknown_3",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_3 = Struct("unknown_3",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    reflexive("unknown_3", sbsp_pathfinding_data_unknown_3_unknown_3),
    ENDIAN=">", SIZE=20
    )


sbsp_pathfinding_data_unknown_4 = Struct("unknown_4",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data = Struct("pathfinding_data",
    reflexive("sectors", sbsp_pathfinding_data_sector),
    reflexive("links", sbsp_pathfinding_data_link),
    reflexive("refs", sbsp_pathfinding_data_ref),
    reflexive("bsp_2d_nodes", sbsp_pathfinding_data_bsp_2d_node),
    reflexive("vertices", sbsp_pathfinding_data_vertice),
    reflexive("object_refs", sbsp_pathfinding_data_object_ref),
    reflexive("pathfinding_hints", sbsp_pathfinding_data_pathfinding_hint),
    reflexive("instanced_geometry_refs", sbsp_pathfinding_data_instanced_geometry_ref),
    SInt32("structure_checksum"),
    Pad(12),
    reflexive("unknown_1", sbsp_pathfinding_data_unknown_1),
    reflexive("unknown_2", sbsp_pathfinding_data_unknown_2),
    reflexive("unknown_3", sbsp_pathfinding_data_unknown_3),
    reflexive("unknown_4", sbsp_pathfinding_data_unknown_4),
    ENDIAN=">", SIZE=160
    )


sbsp_background_sound_environment_palette = Struct("background_sound_environment_palette",
    string_id_meta("name"),
    dependency("sound_environment"),
    Float("cutoff_distance"),
    Float("interpolation_speed"),
    dependency("background_sound"),
    dependency("inside_cluster_sound"),
    Float("cutoff_distance_1"),
    Bool32("scale_flags",
        ),
    Float("interior_scale"),
    Float("portal_scale"),
    Float("exterior_scale"),
    Float("interpolation_speed_1"),
    ENDIAN=">", SIZE=84
    )


sbsp_marker = Struct("markers",
    StrLatin1("name", SIZE=32),
    Float("rotation_i"),
    Float("rotation_j"),
    Float("rotation_k"),
    Float("rotation_w"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    ENDIAN=">", SIZE=60
    )


sbsp_light = Struct("lights",
    dependency("light"),
    ENDIAN=">", SIZE=16
    )


sbsp_unknown_6 = Struct("unknown_6",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sbsp_runtime_decal = Struct("runtime_decals",
    SInt16("palette_index"),
    SInt8("yaw"),
    SInt8("pitch"),
    Float("i"),
    Float("j"),
    Float("k"),
    Float("w"),
    Float("x"),
    Float("y"),
    Float("z"),
    Float("scale"),
    ENDIAN=">", SIZE=36
    )


sbsp_environment_object_palette = Struct("environment_object_palette",
    dependency("definition"),
    dependency("model"),
    Bool32("object_type",
        "biped",
        "vehicle",
        "weapon",
        "equipment",
        "terminal",
        "projectile",
        "scenery",
        "machine",
        "control",
        "sound_scenery",
        "crate",
        "creature",
        "giant",
        "effect_scenery",
        ),
    ENDIAN=">", SIZE=36
    )


sbsp_environment_object = Struct("environment_objects",
    StrLatin1("name", SIZE=32),
    Float("rotation_i"),
    Float("rotation_j"),
    Float("rotation_k"),
    Float("rotation_w"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    Float("scale"),
    SInt16("palette_index"),
    SInt16("unknown"),
    SInt32("unique_id"),
    StrLatin1("scenario_object_name", SIZE=32),
    Pad(4),
    ENDIAN=">", SIZE=108
    )


sbsp_instanced_geometry_instance_collision_definition = Struct("collision_definitions",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    Pad(16),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Pad(4),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Pad(4),
    SInt32("unknown_11"),
    Pad(4),
    SInt8("bsp_index"),
    SInt8("unknown_13"),
    SInt16("instanced_geometry_index"),
    Float("unknown_14"),
    SInt32("unknown_15"),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_16"),
    Pad(12),
    Float("unknown_18"),
    ENDIAN=">", SIZE=112
    )


sbsp_instanced_geometry_instance = Struct("instanced_geometry_instances",
    Float("scale"),
    Float("forward_i"),
    Float("forward_j"),
    Float("forward_k"),
    Float("left_i"),
    Float("left_j"),
    Float("left_k"),
    Float("up_i"),
    Float("up_j"),
    Float("up_k"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    SInt16("mesh_index"),
    Bool16("flags",
        ("no_projectile_collision", 1 << 1),
        ),
    SInt16("unknown_yo_index"),
    SInt16("unknown"),
    Pad(4),
    Float("bounding_sphere_x"),
    Float("bounding_sphere_y"),
    Float("bounding_sphere_z"),
    Float("bounding_sphere_radius1"),
    Float("bounding_sphere_radius2"),
    string_id_meta("name"),
    SInt16("pathfinding_policy"),
    SInt16("lightmapping_policy"),
    Pad(4),
    reflexive("collision_definitions", sbsp_instanced_geometry_instance_collision_definition),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    Pad(4),
    ENDIAN=">", SIZE=120
    )


sbsp_decorator = Struct("decorators",
    dependency("decorator"),
    ENDIAN=">", SIZE=16
    )


sbsp_meshe_part = Struct("parts",
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


sbsp_meshe_subpart = Struct("subparts",
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


sbsp_meshe_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_contents",
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_meshe_instanced_geometry_indice = Struct("instanced_geometry_indices",
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    reflexive("instanced_geometry_mesh_contents", sbsp_meshe_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


sbsp_meshe_unknown_water = Struct("unknown_water",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sbsp_meshe = Struct("meshes",
    reflexive("parts", sbsp_meshe_part),
    reflexive("subparts", sbsp_meshe_subpart),
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
    SEnum8("vertex_type", *sbsp_meshe_vertex_type),
    SEnum8("prt_type", *sbsp_meshe_prt_type),
    SEnum8("index_buffer_type", *sbsp_meshe_index_buffer_type),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    reflexive("instanced_geometry_indices", sbsp_meshe_instanced_geometry_indice),
    reflexive("unknown_water", sbsp_meshe_unknown_water),
    ENDIAN=">", SIZE=76
    )


sbsp_compression_info = Struct("compression_info",
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


sbsp_unknown_nodey = Struct("unknown_nodey",
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


sbsp_unknown_9 = Struct("unknown_9",
    SInt16("unknown"),
    SInt16("unknown_1"),
    rawdata_ref("unknown_2"),
    ENDIAN=">", SIZE=24
    )


sbsp_unknown_meshe_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_meshe = Struct("unknown_meshes",
    rawdata_ref("unknown"),
    reflexive("unknown_1", sbsp_unknown_meshe_unknown_1),
    ENDIAN=">", SIZE=32
    )


sbsp_node_map_unknown = Struct("unknown",
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


sbsp_node_map = Struct("node_maps",
    reflexive("unknown", sbsp_node_map_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_11_unknown = Struct("unknown",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


sbsp_unknown_11 = Struct("unknown_11",
    reflexive("unknown", sbsp_unknown_11_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_yo = Struct("unknown_yo",
    Pad(12),
    SInt16("unknown_index"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=16
    )


sbsp_unknown_sound_clusters_a_portal_designator = Struct("portal_designators",
    SInt16("portal_designator"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_a_interior_cluster_indice = Struct("interior_cluster_indices",
    SInt16("interior_cluster_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_a = Struct("unknown_sound_clusters_a",
    SInt16("background_sound_environment_index"),
    SInt16("unknown"),
    reflexive("portal_designators", sbsp_unknown_sound_clusters_a_portal_designator),
    reflexive("interior_cluster_indices", sbsp_unknown_sound_clusters_a_interior_cluster_indice),
    ENDIAN=">", SIZE=28
    )


sbsp_unknown_sound_clusters_b_portal_designator = Struct("portal_designators",
    SInt16("portal_designator"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_b_interior_cluster_indice = Struct("interior_cluster_indices",
    SInt16("interior_cluster_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_b = Struct("unknown_sound_clusters_b",
    SInt16("background_sound_environment_index"),
    SInt16("unknown"),
    reflexive("portal_designators", sbsp_unknown_sound_clusters_b_portal_designator),
    reflexive("interior_cluster_indices", sbsp_unknown_sound_clusters_b_interior_cluster_indice),
    ENDIAN=">", SIZE=28
    )


sbsp_unknown_sound_clusters_c_portal_designator = Struct("portal_designators",
    SInt16("portal_designator"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_c_interior_cluster_indice = Struct("interior_cluster_indices",
    SInt16("interior_cluster_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_c = Struct("unknown_sound_clusters_c",
    SInt16("background_sound_environment_index"),
    SInt16("unknown"),
    reflexive("portal_designators", sbsp_unknown_sound_clusters_c_portal_designator),
    reflexive("interior_cluster_indices", sbsp_unknown_sound_clusters_c_interior_cluster_indice),
    ENDIAN=">", SIZE=28
    )


sbsp_transparent_plane = Struct("transparent_planes",
    SInt16("mesh_index"),
    SInt16("part_index"),
    Float("plane_i"),
    Float("plane_j"),
    Float("plane_k"),
    Float("plane_d"),
    ENDIAN=">", SIZE=20
    )


sbsp_collision_mopp_code_data = Struct("data",
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sbsp_collision_mopp_code = Struct("collision_mopp_codes",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    Pad(4),
    Float("offset_x"),
    Float("offset_y"),
    Float("offset_z"),
    Float("offset_scale"),
    Pad(4),
    SInt32("data_size"),
    UInt32("data_capacity"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    reflexive("data", sbsp_collision_mopp_code_data),
    Pad(4),
    ENDIAN=">", SIZE=64
    )


sbsp_breakable_surface_mopp_code_data = Struct("data",
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sbsp_breakable_surface_mopp_code = Struct("breakable_surface_mopp_codes",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    Pad(4),
    Float("offset_x"),
    Float("offset_y"),
    Float("offset_z"),
    Float("offset_scale"),
    Pad(4),
    SInt32("data_size"),
    UInt32("data_capacity"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    reflexive("data", sbsp_breakable_surface_mopp_code_data),
    Pad(4),
    ENDIAN=">", SIZE=64
    )


sbsp_breakable_surface_key_table = Struct("breakable_surface_key_table",
    SInt16("instanced_geometry_index"),
    SInt8("breakable_surface_index"),
    UInt8("breakable_surface_sub_index"),
    SInt32("seed_surface_index"),
    Float("x0"),
    Float("x1"),
    Float("y0"),
    Float("y1"),
    Float("z0"),
    Float("z1"),
    ENDIAN=">", SIZE=32
    )


sbsp_meshes_1_part = Struct("parts",
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


sbsp_meshes_1_subpart = Struct("subparts",
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


sbsp_meshes_1_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_contents",
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_meshes_1_instanced_geometry_indice = Struct("instanced_geometry_indices",
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    reflexive("instanced_geometry_mesh_contents", sbsp_meshes_1_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


sbsp_meshes_1_unknown_water = Struct("unknown_water",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sbsp_meshes_1 = Struct("meshes_1",
    reflexive("parts", sbsp_meshes_1_part),
    reflexive("subparts", sbsp_meshes_1_subpart),
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
    SEnum8("vertex_type", *sbsp_meshe_vertex_type),
    SEnum8("prt_type", *sbsp_meshe_prt_type),
    SEnum8("index_buffer_type", *sbsp_meshe_index_buffer_type),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    reflexive("instanced_geometry_indices", sbsp_meshes_1_instanced_geometry_indice),
    reflexive("unknown_water", sbsp_meshes_1_unknown_water),
    ENDIAN=">", SIZE=76
    )


sbsp_compression_info_1 = Struct("compression_info_1",
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


sbsp_unknown_nodey_1 = Struct("unknown_nodey_1",
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


sbsp_unknown_17 = Struct("unknown_17",
    SInt16("unknown"),
    SInt16("unknown_1"),
    rawdata_ref("unknown_2"),
    ENDIAN=">", SIZE=24
    )


sbsp_unknown_meshes_1_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_meshes_1 = Struct("unknown_meshes_1",
    rawdata_ref("unknown"),
    reflexive("unknown_1", sbsp_unknown_meshes_1_unknown_1),
    ENDIAN=">", SIZE=32
    )


sbsp_node_maps_1_unknown = Struct("unknown",
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


sbsp_node_maps_1 = Struct("node_maps_1",
    reflexive("unknown", sbsp_node_maps_1_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_19_unknown = Struct("unknown",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


sbsp_unknown_19 = Struct("unknown_19",
    reflexive("unknown", sbsp_unknown_19_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_yo_1 = Struct("unknown_yo_1",
    Pad(12),
    SInt16("unknown_index"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=16
    )


sbsp_leaf_system = Struct("leaf_systems",
    SInt16("unknown"),
    SInt16("unknown_1"),
    dependency("leaf_system"),
    ENDIAN=">", SIZE=20
    )


sbsp_meta_def = BlockDef("sbsp",
    SInt32("bsp_checksum"),
    SInt32("unknown"),
    Pad(4),
    reflexive("structure_seams", sbsp_structure_seam),
    reflexive("unknown_raw_7th", sbsp_unknown_raw_7th),
    reflexive("collision_materials", sbsp_collision_material),
    reflexive("unknown_raw_3rd", sbsp_unknown_raw_3rd),
    Float("world_bounds_x_min"),
    Float("world_bounds_x_max"),
    Float("world_bounds_y_min"),
    Float("world_bounds_y_max"),
    Float("world_bounds_z_min"),
    Float("world_bounds_z_max"),
    reflexive("unknown_raw_6th", sbsp_unknown_raw_6th),
    reflexive("unknown_1", sbsp_unknown_1),
    reflexive("cluster_portals", sbsp_cluster_portal),
    reflexive("unknown_2", sbsp_unknown_2),
    reflexive("fog", sbsp_fog),
    reflexive("camera_effects", sbsp_camera_effect),
    Pad(12),
    reflexive("detail_objects", sbsp_detail_object),
    reflexive("clusters", sbsp_cluster),
    reflexive("materials", sbsp_material),
    reflexive("sky_owner_cluster", sbsp_sky_owner_cluster),
    reflexive("conveyor_surfaces", sbsp_conveyor_surface),
    reflexive("breakable_surfaces", sbsp_breakable_surface),
    reflexive("pathfinding_data", sbsp_pathfinding_data),
    Pad(12),
    reflexive("background_sound_environment_palette", sbsp_background_sound_environment_palette),
    Pad(44),
    reflexive("markers", sbsp_marker),
    reflexive("lights", sbsp_light),
    reflexive("unknown_6", sbsp_unknown_6),
    reflexive("runtime_decals", sbsp_runtime_decal),
    reflexive("environment_object_palette", sbsp_environment_object_palette),
    reflexive("environment_objects", sbsp_environment_object),
    Pad(40),
    reflexive("instanced_geometry_instances", sbsp_instanced_geometry_instance),
    reflexive("decorators", sbsp_decorator),
    SInt32("unknown_8"),
    reflexive("meshes", sbsp_meshe),
    reflexive("compression_info", sbsp_compression_info),
    reflexive("unknown_nodey", sbsp_unknown_nodey),
    reflexive("unknown_9", sbsp_unknown_9),
    Pad(12),
    reflexive("unknown_meshes", sbsp_unknown_meshe),
    reflexive("node_maps", sbsp_node_map),
    reflexive("unknown_11", sbsp_unknown_11),
    Pad(12),
    reflexive("unknown_yo", sbsp_unknown_yo),
    UInt16("zone_asset_salt_1"),
    UInt16("zone_asset_index_1"),
    SInt32("useless_padding"),
    reflexive("unknown_sound_clusters_a", sbsp_unknown_sound_clusters_a),
    reflexive("unknown_sound_clusters_b", sbsp_unknown_sound_clusters_b),
    reflexive("unknown_sound_clusters_c", sbsp_unknown_sound_clusters_c),
    reflexive("transparent_planes", sbsp_transparent_plane),
    Pad(12),
    reflexive("collision_mopp_codes", sbsp_collision_mopp_code),
    Pad(4),
    Float("collision_world_bounds_x_min"),
    Float("collision_world_bounds_y_min"),
    Float("collision_world_bounds_z_min"),
    Float("collision_world_bounds_x_max"),
    Float("collision_world_bounds_y_max"),
    Float("collision_world_bounds_z_max"),
    reflexive("breakable_surface_mopp_codes", sbsp_breakable_surface_mopp_code),
    reflexive("breakable_surface_key_table", sbsp_breakable_surface_key_table),
    Pad(24),
    SInt32("unknown_16"),
    reflexive("meshes_1", sbsp_meshes_1),
    reflexive("compression_info_1", sbsp_compression_info_1),
    reflexive("unknown_nodey_1", sbsp_unknown_nodey_1),
    reflexive("unknown_17", sbsp_unknown_17),
    Pad(12),
    reflexive("unknown_meshes_1", sbsp_unknown_meshes_1),
    reflexive("node_maps_1", sbsp_node_maps_1),
    reflexive("unknown_19", sbsp_unknown_19),
    Pad(12),
    reflexive("unknown_yo_1", sbsp_unknown_yo_1),
    UInt16("zone_asset_salt_2"),
    UInt16("zone_asset_index_2"),
    SInt32("useless_padding_1"),
    reflexive("leaf_systems", sbsp_leaf_system),
    Pad(12),
    UInt16("zone_asset_salt_3"),
    UInt16("zone_asset_index_3"),
    SInt32("useless_padding_2"),
    SInt32("unknown_22"),
    TYPE=Struct, ENDIAN=">", SIZE=904
    )