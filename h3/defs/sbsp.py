############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Standardized model data and updated
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


sbsp_structure_seam_unknown = Struct("unknown", 
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


sbsp_structure_seam_seam_cluster = Struct("seam_cluster", 
    SInt32("cluster_index"),
    QStruct("centroid", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=16
    )


sbsp_structure_seam = Struct("structure_seam", 
    Array("unknown_array", SUB_STRUCT=UInt32("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("unknown", sbsp_structure_seam_unknown),
    h3_reflexive("seam_clusters", sbsp_structure_seam_seam_cluster),
    ENDIAN=">", SIZE=40
    )


sbsp_unknown_raw_7th = Struct("unknown_raw_7th", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_collision_material = Struct("collision_material", 
    h3_dependency("shader"),
    SInt16("global_material_index"),
    SInt16("conveyor_surface_index"),
    SInt16("seam_index"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


sbsp_unknown_raw_3rd = Struct("unknown_raw_3rd", 
    SInt8("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=1
    )


sbsp_unknown_raw_6th = Struct("unknown_raw_6th", 
    SInt16("unknown_1_start_index", VISIBLE=False),
    SInt16("unknown_1_entry_count", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_unknown_1 = Struct("unknown_1", 
    UInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_cluster_portal_vertice = Struct("vertice", 
    QStruct("position", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=12
    )


sbsp_cluster_portal = Struct("portal", 
    SInt16("portal_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_2 = Struct("unknown_2", 
    BytesRaw("unknown", SIZE=120, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=120
    )


sbsp_fog = Struct("fog", 
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


sbsp_camera_effect = Struct("camera_effect", 
    h3_string_id("name"),
    h3_dependency("effect"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    BytesRaw("unknown_4", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


sbsp_detail_object_unknown_1_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


sbsp_detail_object_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown_0", sbsp_detail_object_unknown_1_unknown_0),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


sbsp_detail_object = Struct("detail_object", 
    BytesRaw("unknown_0", SIZE=28, VISIBLE=False),
    h3_reflexive("unknown_1", sbsp_detail_object_unknown_1),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=52
    )


sbsp_cluster_collision_mopp_code_data = Struct("data", 
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sbsp_cluster_collision_mopp_code = Struct("collision_mopp_code", 
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    QStruct("offset_1", INCLUDE=xyz_float),
    Float("offset_scale"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt32("data_size"),
    UInt32("data_capacity"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("data", sbsp_cluster_collision_mopp_code_data),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


sbsp_cluster_seam = Struct("seam", 
    SInt8("seam_index"),
    ENDIAN=">", SIZE=1
    )


sbsp_cluster_decorator_grid = Struct("decorator_grid", 
    SInt16("amount"),
    SInt8("decorator_index"),
    SInt8("decorator_index_scattering"),
    SInt32("unknown", VISIBLE=False),
    QStruct("position", INCLUDE=xyz_float),
    Float("radius"),
    QStruct("grid_size", INCLUDE=xyz_float),
    QStruct("bounding_sphere", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=48
    )


sbsp_cluster_unknown_11 = Struct("unknown_11", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_cluster_unknown_12 = Struct("unknown_12", 
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


sbsp_cluster = Struct("cluster", 
    QStruct("bounds_x", INCLUDE=from_to),
    QStruct("bounds_y", INCLUDE=from_to),
    QStruct("bounds_z", INCLUDE=from_to),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("scenario_sky_index"),
    SInt8("camera_effect_index"),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("background_sound_environment_index"),
    SInt16("sound_clusters_a_index", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=5, VISIBLE=False),
    SInt16("runtime_decal_start_index"),
    SInt16("runtime_decal_entry_count"),
    SInt16("flags"),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    h3_reflexive("portals", sbsp_cluster_portal),
    SInt32("unknown_3", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_4", VISIBLE=False),
    BytesRaw("unknown_5", SIZE=8, VISIBLE=False),
    h3_dependency("bsp"),
    SInt32("cluster_index"),
    SInt32("unknown_6", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_7", VISIBLE=False),
    BytesRaw("unknown_8", SIZE=12, VISIBLE=False),
    h3_reflexive("collision_mopp_codes", sbsp_cluster_collision_mopp_code),
    SInt16("mesh_index"),
    SInt16("unknown_9", VISIBLE=False),
    h3_reflexive("seams", sbsp_cluster_seam),
    h3_reflexive("decorator_grids", sbsp_cluster_decorator_grid),
    BytesRaw("unknown_10", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_11", sbsp_cluster_unknown_11),
    h3_reflexive("unknown_12", sbsp_cluster_unknown_12),
    ENDIAN=">", SIZE=220
    )


sbsp_material_propertie = Struct("propertie", 
    SInt16("type"),
    SInt16("int_value"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    Float("real_value"),
    ENDIAN=">", SIZE=12
    )


sbsp_material = Struct("material", 
    h3_dependency("shader"),
    h3_reflexive("properties", sbsp_material_propertie),
    SInt32("unknown_0", VISIBLE=False),
    SInt8("breakable_surface_index"),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    SInt8("unknown_3", VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


sbsp_sky_owner_cluster = Struct("sky_owner_cluster", 
    SInt16("cluster_owner"),
    ENDIAN=">", SIZE=2
    )


sbsp_conveyor_surface = Struct("conveyor_surface", 
    BytesRaw("u_i", SIZE=24, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


sbsp_breakable_surface = Struct("breakable_surface", 
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


sbsp_pathfinding_data_sector = Struct("sector", 
    Bool16("pathfinding_sector_flags", 
        "sector_walkable",
        ("sector_bsp_source", 1 << 3),
        "floor",
        ),
    SInt16("hint_index"),
    SInt32("first_link"),
    ENDIAN=">", SIZE=8
    )


sbsp_pathfinding_data_link = Struct("link", 
    SInt16("vertex_1"),
    SInt16("vertex_2"),
    Bool16("link_flags", *unknown_flags_16),
    SInt16("hint_index"),
    SInt16("forward_link"),
    SInt16("reverse_link"),
    SInt16("left_sector"),
    SInt16("right_sector"),
    ENDIAN=">", SIZE=16
    )


sbsp_pathfinding_data_ref = Struct("ref", 
    SInt32("node_or_sector_ref"),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_bsp_2d_node = Struct("bsp_2d_node", 
    Pad(12),
    SInt32("left_child"),
    SInt32("right_child"),
    ENDIAN=">", SIZE=20
    )


sbsp_pathfinding_data_vertice = Struct("vertice", 
    Pad(12),
    ENDIAN=">", SIZE=12
    )


sbsp_pathfinding_data_object_ref_unknown_1_unknown_1 = Struct("unknown_1", 
    SInt32("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_object_ref_unknown_1 = Struct("unknown_1", 
    Pad(8),
    h3_reflexive("unknown_1", sbsp_pathfinding_data_object_ref_unknown_1_unknown_1),
    SInt32("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


sbsp_pathfinding_data_object_ref = Struct("object_ref", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", sbsp_pathfinding_data_object_ref_unknown_1),
    SInt32("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


sbsp_pathfinding_data_pathfinding_hint = Struct("pathfinding_hint", 
    SInt16("next_hint_index"),
    Pad(2),
    Array("hint_data_array", SUB_STRUCT=SInt16("hint_data"), SIZE=8),
    ENDIAN=">", SIZE=20
    )


sbsp_pathfinding_data_instanced_geometry_ref = Struct("instanced_geometry_ref", 
    SInt16("pathfinding_object_index"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_2_unknown = Struct("unknown", 
    SInt32("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_2 = Struct("unknown_2", 
    h3_reflexive("unknown", sbsp_pathfinding_data_unknown_2_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


sbsp_pathfinding_data_unknown_3_unknown_3 = Struct("unknown_3", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data_unknown_3 = Struct("unknown_3", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    h3_reflexive("unknown_3", sbsp_pathfinding_data_unknown_3_unknown_3),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


sbsp_pathfinding_data_unknown_4 = Struct("unknown_4", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sbsp_pathfinding_data = Struct("pathfinding_data", 
    h3_reflexive("sectors", sbsp_pathfinding_data_sector),
    h3_reflexive("links", sbsp_pathfinding_data_link),
    h3_reflexive("refs", sbsp_pathfinding_data_ref),
    h3_reflexive("bsp_2d_nodes", sbsp_pathfinding_data_bsp_2d_node),
    h3_reflexive("vertices", sbsp_pathfinding_data_vertice),
    h3_reflexive("object_refs", sbsp_pathfinding_data_object_ref),
    h3_reflexive("pathfinding_hints", sbsp_pathfinding_data_pathfinding_hint),
    h3_reflexive("instanced_geometry_refs", sbsp_pathfinding_data_instanced_geometry_ref),
    SInt32("structure_checksum"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_1", sbsp_pathfinding_data_unknown_1),
    h3_reflexive("unknown_2", sbsp_pathfinding_data_unknown_2),
    h3_reflexive("unknown_3", sbsp_pathfinding_data_unknown_3),
    h3_reflexive("unknown_4", sbsp_pathfinding_data_unknown_4),
    ENDIAN=">", SIZE=160
    )


sbsp_background_sound_environment_palette = Struct("background_sound_environment_palette", 
    h3_string_id("name"),
    h3_dependency("sound_environment"),
    Float("cutoff_distance_0"),
    Float("interpolation_speed_0"),
    h3_dependency("background_sound"),
    h3_dependency("inside_cluster_sound"),
    Float("cutoff_distance_1"),
    Bool32("scale_flags", *unknown_flags_32),
    Float("interior_scale"),
    Float("portal_scale"),
    Float("exterior_scale"),
    Float("interpolation_speed_1"),
    ENDIAN=">", SIZE=84
    )


sbsp_marker = Struct("marker", 
    ascii_str32("name"),
    QStruct("rotation", INCLUDE=ijkw_float),
    QStruct("position", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=60
    )


sbsp_light = Struct("light", 
    h3_dependency("light"),
    ENDIAN=">", SIZE=16
    )


sbsp_unknown_6 = Struct("unknown_6", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sbsp_runtime_decal = Struct("runtime_decal", 
    SInt16("palette_index"),
    SInt8("yaw"),
    SInt8("pitch"),
    QStruct("rotation", INCLUDE=ijkw_float),
    QStruct("position", INCLUDE=xyz_float),
    Float("scale"),
    ENDIAN=">", SIZE=36
    )


sbsp_environment_object_palette = Struct("environment_object_palette", 
    h3_dependency("definition"),
    h3_dependency("model"),
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


sbsp_environment_object = Struct("environment_object", 
    ascii_str32("name"),
    QStruct("rotation", INCLUDE=ijkw_float),
    QStruct("position", INCLUDE=xyz_float),
    Float("scale"),
    SInt16("palette_index"),
    SInt16("unknown_0", VISIBLE=False),
    SInt32("unique_id"),
    ascii_str32("scenario_object_name"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=108
    )


sbsp_instanced_geometry_instance_collision_definition = Struct("collision_definition", 
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0", VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=16, VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    Float("unknown_4", VISIBLE=False),
    Float("unknown_5", VISIBLE=False),
    BytesRaw("unknown_6", SIZE=4, VISIBLE=False),
    Float("unknown_7", VISIBLE=False),
    Float("unknown_8", VISIBLE=False),
    Float("unknown_9", VISIBLE=False),
    BytesRaw("unknown_10", SIZE=4, VISIBLE=False),
    SInt32("unknown_11", VISIBLE=False),
    BytesRaw("unknown_12", SIZE=4, VISIBLE=False),
    SInt8("bsp_index"),
    SInt8("unknown_13", VISIBLE=False),
    SInt16("instanced_geometry_index"),
    Float("unknown_14", VISIBLE=False),
    SInt32("unknown_15", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1", VISIBLE=False),
    SInt32("unknown_16", VISIBLE=False),
    BytesRaw("unknown_17", SIZE=12, VISIBLE=False),
    Float("unknown_18", VISIBLE=False),
    ENDIAN=">", SIZE=112
    )


sbsp_instanced_geometry_instance = Struct("instanced_geometry_instance", 
    Float("scale"),
    QStruct("forward", INCLUDE=ijk_float),
    QStruct("left", INCLUDE=ijk_float),
    QStruct("up", INCLUDE=ijk_float),
    QStruct("position", INCLUDE=xyz_float),
    SInt16("mesh_index"),
    Bool16("flags", 
        ("no_projectile_collision", 1 << 1),
        ),
    SInt16("unknown_yo_index", VISIBLE=False),
    SInt16("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    QStruct("bounding_sphere", INCLUDE=xyz_float),
    Float("bounding_sphere_radius1"),
    Float("bounding_sphere_radius2"),
    h3_string_id("name"),
    SInt16("pathfinding_policy"),
    SInt16("lightmapping_policy"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    h3_reflexive("collision_definitions", sbsp_instanced_geometry_instance_collision_definition),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


sbsp_decorator = Struct("decorator", 
    h3_dependency("decorator"),
    ENDIAN=">", SIZE=16
    )


sbsp_meshes_0_part = Struct("part", 
    SInt16("material_index"),
    SInt16("unknown_nodey_index", VISIBLE=False),
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("subpart_index"),
    SInt16("subpart_count"),
    SInt8("unknown_enum", VISIBLE=False),
    Bool8("flags", 
        ("water", 1 << 3),
        ),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=16
    )


sbsp_meshes_0_subpart = Struct("subpart", 
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


sbsp_meshes_0_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_content", 
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_meshes_0_instanced_geometry_indice = Struct("instanced_geometry_indice", 
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    h3_reflexive("instanced_geometry_mesh_contents", sbsp_meshes_0_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


sbsp_meshes_0_unknown_water = Struct("unknown_water", 
    SInt16("unknown"),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sbsp_meshes_0 = Struct("meshes_0", 
    h3_reflexive("parts", sbsp_meshes_0_part),
    h3_reflexive("subparts", sbsp_meshes_0_subpart),
    Array("vertex_buffer_index_array", SUB_STRUCT=SInt16("vertex_buffer_index"), SIZE=8),
    SInt16("index_buffer_index_1"),
    SInt16("index_buffer_index_2"),
    Bool8("flags", 
        "has_vertex_colors",
        ),
    SInt8("rigid_node"),
    SEnum8("vertex_type", *pmdf_meshe_vertex_type),
    SEnum8("prt_type", *pmdf_meshe_prt_type),
    SEnum8("index_buffer_type", *pmdf_meshe_index_buffer_type),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    h3_reflexive("instanced_geometry_indices", sbsp_meshes_0_instanced_geometry_indice),
    h3_reflexive("unknown_water", sbsp_meshes_0_unknown_water),
    ENDIAN=">", SIZE=76
    )


sbsp_compression_info_0 = Struct("compression_info_0", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    QStruct("position_bounds_x", INCLUDE=from_to),
    QStruct("position_bounds_y", INCLUDE=from_to),
    QStruct("position_bounds_z", INCLUDE=from_to),
    QStruct("texcoord_bounds_x", INCLUDE=from_to),
    QStruct("texcoord_bounds_y", INCLUDE=from_to),
    ENDIAN=">", SIZE=44
    )


sbsp_unknown_nodey_0 = Struct("unknown_nodey_0", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    Array("node_index_array", SUB_STRUCT=SInt8("node_index"), SIZE=4, VISIBLE=False),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


sbsp_unknown_9 = Struct("unknown_9", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_rawdata_ref("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


sbsp_unknown_meshes_0_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_meshes_0 = Struct("unknown_meshes_0", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", sbsp_unknown_meshes_0_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


sbsp_node_maps_0_unknown = Struct("unknown", 
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


sbsp_node_maps_0 = Struct("node_maps_0", 
    h3_reflexive("unknown", sbsp_node_maps_0_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_11_unknown = Struct("unknown", 
    BytesRaw("unknown", SIZE=48, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


sbsp_unknown_11 = Struct("unknown_11", 
    h3_reflexive("unknown", sbsp_unknown_11_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_yo_0 = Struct("unknown_yo_0", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt16("unknown_index"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


sbsp_unknown_sound_clusters_a_portal_designator = Struct("portal_designator", 
    SInt16("portal_designator"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_a_interior_cluster_indice = Struct("interior_cluster_indice", 
    SInt16("interior_cluster_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_a = Struct("unknown_sound_clusters_a", 
    SInt16("background_sound_environment_index"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("portal_designators", sbsp_unknown_sound_clusters_a_portal_designator),
    h3_reflexive("interior_cluster_indices", sbsp_unknown_sound_clusters_a_interior_cluster_indice),
    ENDIAN=">", SIZE=28
    )


sbsp_unknown_sound_clusters_b_portal_designator = Struct("portal_designator", 
    SInt16("portal_designator"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_b_interior_cluster_indice = Struct("interior_cluster_indice", 
    SInt16("interior_cluster_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_b = Struct("unknown_sound_clusters_b", 
    SInt16("background_sound_environment_index"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("portal_designators", sbsp_unknown_sound_clusters_b_portal_designator),
    h3_reflexive("interior_cluster_indices", sbsp_unknown_sound_clusters_b_interior_cluster_indice),
    ENDIAN=">", SIZE=28
    )


sbsp_unknown_sound_clusters_c_portal_designator = Struct("portal_designator", 
    SInt16("portal_designator"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_c_interior_cluster_indice = Struct("interior_cluster_indice", 
    SInt16("interior_cluster_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_sound_clusters_c = Struct("unknown_sound_clusters_c", 
    SInt16("background_sound_environment_index"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("portal_designators", sbsp_unknown_sound_clusters_c_portal_designator),
    h3_reflexive("interior_cluster_indices", sbsp_unknown_sound_clusters_c_interior_cluster_indice),
    ENDIAN=">", SIZE=28
    )


sbsp_transparent_plane = Struct("transparent_plane", 
    SInt16("mesh_index"),
    SInt16("part_index"),
    QStruct("plane", INCLUDE=ijk_float),
    Float("plane_d"),
    ENDIAN=">", SIZE=20
    )


sbsp_collision_mopp_code_data = Struct("data", 
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sbsp_collision_mopp_code = Struct("collision_mopp_code", 
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    QStruct("offset_1", INCLUDE=xyz_float),
    Float("offset_scale"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt32("data_size"),
    UInt32("data_capacity"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("data", sbsp_collision_mopp_code_data),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


sbsp_breakable_surface_mopp_code_data = Struct("data", 
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sbsp_breakable_surface_mopp_code = Struct("breakable_surface_mopp_code", 
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    QStruct("offset_1", INCLUDE=xyz_float),
    Float("offset_scale"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt32("data_size"),
    UInt32("data_capacity"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("data", sbsp_breakable_surface_mopp_code_data),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
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


sbsp_meshes_1_part = Struct("part", 
    SInt16("material_index"),
    SInt16("unknown_nodey_index", VISIBLE=False),
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("subpart_index"),
    SInt16("subpart_count"),
    SInt8("unknown_enum", VISIBLE=False),
    Bool8("flags", 
        ("water", 1 << 3),
        ),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=16
    )


sbsp_meshes_1_subpart = Struct("subpart", 
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


sbsp_meshes_1_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_content", 
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


sbsp_meshes_1_instanced_geometry_indice = Struct("instanced_geometry_indice", 
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    h3_reflexive("instanced_geometry_mesh_contents", sbsp_meshes_1_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


sbsp_meshes_1_unknown_water = Struct("unknown_water", 
    SInt16("unknown"),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sbsp_meshes_1 = Struct("meshes_1", 
    h3_reflexive("parts", sbsp_meshes_1_part),
    h3_reflexive("subparts", sbsp_meshes_1_subpart),
    Array("vertex_buffer_index_array", SUB_STRUCT=SInt16("vertex_buffer_index"), SIZE=8),
    SInt16("index_buffer_index_1"),
    SInt16("index_buffer_index_2"),
    Bool8("flags", 
        "has_vertex_colors",
        ),
    SInt8("rigid_node"),
    SEnum8("vertex_type", *pmdf_meshe_vertex_type),
    SEnum8("prt_type", *pmdf_meshe_prt_type),
    SEnum8("index_buffer_type", *pmdf_meshe_index_buffer_type),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    h3_reflexive("instanced_geometry_indices", sbsp_meshes_1_instanced_geometry_indice),
    h3_reflexive("unknown_water", sbsp_meshes_1_unknown_water),
    ENDIAN=">", SIZE=76
    )


sbsp_compression_info_1 = Struct("compression_info_1", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    QStruct("position_bounds_x", INCLUDE=from_to),
    QStruct("position_bounds_y", INCLUDE=from_to),
    QStruct("position_bounds_z", INCLUDE=from_to),
    QStruct("texcoord_bounds_x", INCLUDE=from_to),
    QStruct("texcoord_bounds_y", INCLUDE=from_to),
    ENDIAN=">", SIZE=44
    )


sbsp_unknown_nodey_1 = Struct("unknown_nodey_1", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    Array("node_index_array", SUB_STRUCT=SInt8("node_index"), SIZE=4, VISIBLE=False),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


sbsp_unknown_17 = Struct("unknown_17", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_rawdata_ref("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


sbsp_unknown_meshes_1_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sbsp_unknown_meshes_1 = Struct("unknown_meshes_1", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", sbsp_unknown_meshes_1_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


sbsp_node_maps_1_unknown = Struct("unknown", 
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


sbsp_node_maps_1 = Struct("node_maps_1", 
    h3_reflexive("unknown", sbsp_node_maps_1_unknown),
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_19_unknown = Struct("unknown", 
    BytesRaw("unknown", SIZE=48, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


sbsp_unknown_19 = Struct("unknown_19", 
    h3_reflexive("unknown", sbsp_unknown_19_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


sbsp_unknown_yo_1 = Struct("unknown_yo_1", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt16("unknown_index"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


sbsp_leaf_system = Struct("leaf_system", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_dependency("leaf_system"),
    ENDIAN=">", SIZE=20
    )


sbsp_body = Struct("tagdata", 
    SInt32("bsp_checksum"),
    SInt32("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("structure_seams", sbsp_structure_seam),
    h3_reflexive("unknown_raw_7th", sbsp_unknown_raw_7th),
    h3_reflexive("collision_materials", sbsp_collision_material),
    h3_reflexive("unknown_raw_3rd", sbsp_unknown_raw_3rd),
    QStruct("world_bounds_x", INCLUDE=from_to),
    QStruct("world_bounds_y", INCLUDE=from_to),
    QStruct("world_bounds_z", INCLUDE=from_to),
    h3_reflexive("unknown_raw_6th", sbsp_unknown_raw_6th),
    h3_reflexive("unknown_2", sbsp_unknown_1),
    h3_reflexive("cluster_portals", sbsp_cluster_portal),
    h3_reflexive("unknown_3", sbsp_unknown_2),
    h3_reflexive("fog", sbsp_fog),
    h3_reflexive("camera_effects", sbsp_camera_effect),
    BytesRaw("unknown_4", SIZE=12, VISIBLE=False),
    h3_reflexive("detail_objects", sbsp_detail_object),
    h3_reflexive("clusters", sbsp_cluster),
    h3_reflexive("materials", sbsp_material),
    h3_reflexive("sky_owner_cluster", sbsp_sky_owner_cluster),
    h3_reflexive("conveyor_surfaces", sbsp_conveyor_surface),
    h3_reflexive("breakable_surfaces", sbsp_breakable_surface),
    h3_reflexive("pathfinding_data", sbsp_pathfinding_data),
    BytesRaw("unknown_5", SIZE=12, VISIBLE=False),
    h3_reflexive("background_sound_environment_palette", sbsp_background_sound_environment_palette),
    BytesRaw("unknown_6", SIZE=44, VISIBLE=False),
    h3_reflexive("markers", sbsp_marker),
    h3_reflexive("lights", sbsp_light),
    h3_reflexive("unknown_7", sbsp_unknown_6),
    h3_reflexive("runtime_decals", sbsp_runtime_decal),
    h3_reflexive("environment_object_palette", sbsp_environment_object_palette),
    h3_reflexive("environment_objects", sbsp_environment_object),
    BytesRaw("unknown_8", SIZE=40, VISIBLE=False),
    h3_reflexive("instanced_geometry_instances", sbsp_instanced_geometry_instance),
    h3_reflexive("decorators", sbsp_decorator),
    SInt32("unknown_9", VISIBLE=False),
    h3_reflexive("meshes_0", sbsp_meshes_0),
    h3_reflexive("compression_info_0", sbsp_compression_info_0),
    h3_reflexive("unknown_nodey_0", sbsp_unknown_nodey_0),
    h3_reflexive("unknown_10", sbsp_unknown_9),
    BytesRaw("unknown_11", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_meshes_0", sbsp_unknown_meshes_0),
    h3_reflexive("node_maps_0", sbsp_node_maps_0),
    h3_reflexive("unknown_12", sbsp_unknown_11),
    BytesRaw("unknown_13", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_yo_0", sbsp_unknown_yo_0),
    zone_asset("asset_data_0"),
    h3_reflexive("unknown_sound_clusters_a", sbsp_unknown_sound_clusters_a),
    h3_reflexive("unknown_sound_clusters_b", sbsp_unknown_sound_clusters_b),
    h3_reflexive("unknown_sound_clusters_c", sbsp_unknown_sound_clusters_c),
    h3_reflexive("transparent_planes", sbsp_transparent_plane),
    BytesRaw("unknown_14", SIZE=12, VISIBLE=False),
    h3_reflexive("collision_mopp_codes", sbsp_collision_mopp_code),
    BytesRaw("unknown_15", SIZE=4, VISIBLE=False),
    Float("collision_world_bounds_x_min"),
    Float("collision_world_bounds_y_min"),
    Float("collision_world_bounds_z_min"),
    Float("collision_world_bounds_x_max"),
    Float("collision_world_bounds_y_max"),
    Float("collision_world_bounds_z_max"),
    h3_reflexive("breakable_surface_mopp_codes", sbsp_breakable_surface_mopp_code),
    h3_reflexive("breakable_surface_key_table", sbsp_breakable_surface_key_table),
    BytesRaw("unknown_16", SIZE=24, VISIBLE=False),
    SInt32("unknown_17", VISIBLE=False),
    h3_reflexive("meshes_1", sbsp_meshes_1),
    h3_reflexive("compression_info_1", sbsp_compression_info_1),
    h3_reflexive("unknown_nodey_1", sbsp_unknown_nodey_1),
    h3_reflexive("unknown_18", sbsp_unknown_17),
    BytesRaw("unknown_19", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_meshes_1", sbsp_unknown_meshes_1),
    h3_reflexive("node_maps_1", sbsp_node_maps_1),
    h3_reflexive("unknown_20", sbsp_unknown_19),
    BytesRaw("unknown_21", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_yo_1", sbsp_unknown_yo_1),
    zone_asset("asset_data_1"),
    h3_reflexive("leaf_systems", sbsp_leaf_system),
    BytesRaw("unknown_22", SIZE=12, VISIBLE=False),
    UInt16("zone_asset_salt_3"),
    UInt16("zone_asset_index_3"),
    SInt32("useless_padding_2", VISIBLE=False),
    SInt32("unknown_23", VISIBLE=False),
    ENDIAN=">", SIZE=904
    )


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    h3_blam_header('sbsp'),
    sbsp_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["sbsp"], endian=">", tag_cls=H3Tag
    )
