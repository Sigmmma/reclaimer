from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

phmo_list_shape_shape_type = (
    "sphere",
    "pill",
    "box",
    "triangle",
    "polyhedron",
    "multi_sphere",
    "unknown_shape",
    "unused_1",
    "unused_2",
    "unused_3",
    "unused_4",
    "unused_5",
    "unused_6",
    "unused_7",
    "list",
    "mopp",
    )

phmo_node_edge_constraint_type = (
    "hinge",
    "limited_hinge",
    "ragdoll",
    "stiff_spring",
    "ball_and_socket",
    "prismatic",
    )

phmo_phantom_type_minimum_size = (
    "default",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "extra_huge",
    )

phmo_rigid_bodie_motion_type = (
    "sphere",
    "stabilized_sphere",
    "box",
    "stabilized_box",
    "keyframed",
    "fixed",
    )

phmo_rigid_bodie_shape_type = (
    "sphere",
    "pill",
    "box",
    "triangle",
    "polyhedron",
    "multi_sphere",
    "unused_0",
    "unused_1",
    "unused_2",
    "unused_3",
    "unused_4",
    "unused_5",
    "unused_6",
    "unused_7",
    "list",
    "mopp",
    )


phmo_unknown_6 = Struct("unknown_6",
    string_id_meta("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Pad(4),
    ENDIAN=">", SIZE=24
    )


phmo_unknown_7 = Struct("unknown_7",
    string_id_meta("name"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Pad(8),
    ENDIAN=">", SIZE=32
    )


phmo_phantom_type = Struct("phantom_types",
    Bool32("flags",
        "generates_effects",
        "use_acceleration_as_force",
        "negates_gravity",
        "ignores_players",
        "ignores_nonplayers",
        "ignores_bipeds",
        "ignores_vehicles",
        "ignores_weapons",
        "ignores_equipment",
        "ignores_terminals",
        "ignores_projectiles",
        "ignores_scenery",
        "ignores_machines",
        "ignores_controls",
        "ignores_sound_scenery",
        "ignores_crates",
        "ignores_creatures",
        "ignores_giants",
        "ignores_effect_scenery",
        ),
    SEnum8("minimum_size", *phmo_phantom_type_minimum_size),
    SEnum8("maximum_size", *phmo_phantom_type_minimum_size),
    SInt16("unknown"),
    string_id_meta("marker_name"),
    string_id_meta("alignment_marker_name"),
    Pad(8),
    Float("hooke_s_law_e"),
    Float("linear_dead_radius"),
    Float("center_acceleration"),
    Float("center_max_velocity"),
    Float("axis_acceleration"),
    Float("axis_max_velocity"),
    Float("direction_acceleration"),
    Float("direction_max_velocity"),
    Pad(28),
    Float("alignment_hooke_s_law_e"),
    float_rad("alignment_acceleration"),
    float_rad("alignment_max_velocity"),
    Pad(8),
    ENDIAN=">", SIZE=104
    )


phmo_unknown_8_unknown = Struct("unknown",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


phmo_unknown_8_unknown_1 = Struct("unknown_1",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


phmo_unknown_8 = Struct("unknown_8",
    reflexive("unknown", phmo_unknown_8_unknown),
    reflexive("unknown_1", phmo_unknown_8_unknown_1),
    ENDIAN=">", SIZE=24
    )


phmo_node_edge_constraint_unknown = Struct("unknown",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    ENDIAN=">", SIZE=12
    )


phmo_node_edge_constraint_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


phmo_node_edge_constraint = Struct("constraints",
    SEnum16("type", *phmo_node_edge_constraint_type),
    SInt16("idx"),
    Bool32("flags",
        ),
    Float("friction"),
    reflexive("unknown", phmo_node_edge_constraint_unknown),
    reflexive("unknown_1", phmo_node_edge_constraint_unknown_1),
    ENDIAN=">", SIZE=36
    )


phmo_node_edge = Struct("node_edges",
    SInt16("node_a_global_material_index"),
    SInt16("node_b_global_material_index"),
    SInt16("node_a"),
    SInt16("node_b"),
    reflexive("constraints", phmo_node_edge_constraint),
    string_id_meta("node_a_material"),
    string_id_meta("node_b_material"),
    ENDIAN=">", SIZE=28
    )


phmo_rigid_bodie = Struct("rigid_bodies",
    SInt16("node"),
    SInt16("region"),
    SInt16("permutations"),
    SInt16("unknown"),
    Float("bounding_sphere_offset_x"),
    Float("bounding_sphere_offset_y"),
    Float("bounding_sphere_offset_z"),
    Float("bounding_sphere_radius"),
    Bool16("flags",
        "no_collisions_with_self",
        "only_collide_with_environment",
        "disable_effects",
        "does_not_interact_with_environment",
        "best_early_mover_body",
        "has_no_phantom_power_version",
        "locked_in_place",
        ),
    SEnum16("motion_type", *phmo_rigid_bodie_motion_type),
    SInt16("no_phantom_power_alt_rigid_body"),
    SEnum16("size", *phmo_phantom_type_minimum_size),
    Pad(56),
    SEnum16("shape_type", *phmo_rigid_bodie_shape_type),
    SInt16("shape_index"),
    Pad(84),
    ENDIAN=">", SIZE=176
    )


phmo_material = Struct("materials",
    string_id_meta("name"),
    string_id_meta("material_name"),
    SInt16("phantom_type_index"),
    SInt8("unknown"),
    SInt8("unknown_1"),
    ENDIAN=">", SIZE=12
    )


phmo_sphere = Struct("spheres",
    string_id_meta("name"),
    SInt8("material_index"),
    SInt8("unknown"),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    SInt32("unknown_4"),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_5"),
    Float("radius_1"),
    Pad(12),
    Float("translation_i"),
    Float("translation_j"),
    Float("translation_k"),
    Float("translation_radius"),
    ENDIAN=">", SIZE=112
    )


phmo_pill = Struct("pills",
    string_id_meta("name"),
    SInt8("material_index"),
    SInt8("unknown"),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    Float("bottom_i"),
    Float("bottom_j"),
    Float("bottom_k"),
    Float("bottom_radius"),
    Float("top_i"),
    Float("top_j"),
    Float("top_k"),
    Float("top_radius"),
    ENDIAN=">", SIZE=96
    )


phmo_boxe = Struct("boxes",
    string_id_meta("name"),
    SInt8("material_index"),
    SInt8("unknown"),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    Float("half_extents_i"),
    Float("half_extents_j"),
    Float("half_extents_k"),
    Float("half_extents_radius"),
    SInt32("unknown_4"),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_5"),
    Float("radius_1"),
    Pad(12),
    Float("rotation_i_i"),
    Float("rotation_i_j"),
    Float("rotation_i_k"),
    Float("rotation_i_radius"),
    Float("rotation_j_i"),
    Float("rotation_j_j"),
    Float("rotation_j_k"),
    Float("rotation_j_radius"),
    Float("rotation_k_i"),
    Float("rotation_k_j"),
    Float("rotation_k_k"),
    Float("rotation_k_radius"),
    Float("translation_i"),
    Float("translation_j"),
    Float("translation_k"),
    Float("translation_radius"),
    ENDIAN=">", SIZE=176
    )


phmo_triangle = Struct("triangles",
    string_id_meta("name"),
    SInt8("material_index"),
    SInt8("unknown"),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Pad(80),
    ENDIAN=">", SIZE=128
    )


phmo_polyhedra = Struct("polyhedra",
    string_id_meta("name"),
    SInt8("material_index"),
    SInt8("unknown"),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    Float("aabb_half_extents_i"),
    Float("aabb_half_extents_j"),
    Float("aabb_half_extents_k"),
    Float("aabb_half_extents_radius"),
    Float("aabb_center_i"),
    Float("aabb_center_j"),
    Float("aabb_center_k"),
    Float("aabb_center_radius"),
    Pad(4),
    SInt32("four_vectors_size"),
    UInt32("four_vectors_capacity"),
    SInt32("unknown_5"),
    Pad(4),
    SInt32("plane_equations_size"),
    UInt32("plane_equations_capacity"),
    Pad(4),
    ENDIAN=">", SIZE=128
    )


phmo_polyhedron_four_vector = Struct("polyhedron_four_vectors",
    Float("four_vectors_x_i"),
    Float("four_vectors_x_j"),
    Float("four_vectors_x_k"),
    Float("four_vectors_x_radius"),
    Float("four_vectors_y_i"),
    Float("four_vectors_y_j"),
    Float("four_vectors_y_k"),
    Float("four_vectors_y_radius"),
    Float("four_vectors_z_i"),
    Float("four_vectors_z_j"),
    Float("four_vectors_z_k"),
    Float("four_vectors_z_radius"),
    ENDIAN=">", SIZE=48
    )


phmo_polyhedron_plane_equation = Struct("polyhedron_plane_equations",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    ENDIAN=">", SIZE=16
    )


phmo_list = Struct("lists",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    Pad(12),
    SInt32("child_shapes_size"),
    UInt32("child_shapes_capacity"),
    Pad(12),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    ENDIAN=">", SIZE=80
    )


phmo_list_shape = Struct("list_shapes",
    SEnum16("shape_type", *phmo_list_shape_shape_type),
    SInt16("shape_index"),
    Pad(4),
    UInt32("unknown_1"),
    SInt32("unknown_2"),
    ENDIAN=">", SIZE=16
    )


phmo_mopp = Struct("mopps",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    Pad(4),
    SEnum16("shape_type", *phmo_list_shape_shape_type),
    SInt16("shape_index"),
    Pad(8),
    ENDIAN=">", SIZE=32
    )


phmo_hinge_constraint = Struct("hinge_constraints",
    string_id_meta("name"),
    SInt16("node_a"),
    SInt16("node_b"),
    Float("a_scale"),
    Float("a_forward_i"),
    Float("a_forward_j"),
    Float("a_forward_k"),
    Float("a_left_i"),
    Float("a_left_j"),
    Float("a_left_k"),
    Float("a_up_i"),
    Float("a_up_j"),
    Float("a_up_k"),
    Float("a_position_x"),
    Float("a_position_y"),
    Float("a_position_z"),
    Float("b_scale"),
    Float("b_forward_i"),
    Float("b_forward_j"),
    Float("b_forward_k"),
    Float("b_left_i"),
    Float("b_left_j"),
    Float("b_left_k"),
    Float("b_up_i"),
    Float("b_up_j"),
    Float("b_up_k"),
    Float("b_position_i"),
    Float("b_position_j"),
    Float("b_position_k"),
    SInt16("edge_index"),
    SInt16("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=120
    )


phmo_ragdoll_constraint = Struct("ragdoll_constraints",
    string_id_meta("name"),
    SInt16("node_a"),
    SInt16("node_b"),
    Float("a_scale"),
    Float("a_forward_i"),
    Float("a_forward_j"),
    Float("a_forward_k"),
    Float("a_left_i"),
    Float("a_left_j"),
    Float("a_left_k"),
    Float("a_up_i"),
    Float("a_up_j"),
    Float("a_up_k"),
    Float("a_position_x"),
    Float("a_position_y"),
    Float("a_position_z"),
    Float("b_scale"),
    Float("b_forward_i"),
    Float("b_forward_j"),
    Float("b_forward_k"),
    Float("b_left_i"),
    Float("b_left_j"),
    Float("b_left_k"),
    Float("b_up_i"),
    Float("b_up_j"),
    Float("b_up_k"),
    Float("b_position_x"),
    Float("b_position_y"),
    Float("b_position_z"),
    SInt16("edge_index"),
    SInt16("unknown"),
    Pad(4),
    Float("min_twist"),
    Float("max_twist"),
    Float("min_cone"),
    Float("max_cone"),
    Float("min_plane"),
    Float("max_plane"),
    Float("max_friction_torque"),
    ENDIAN=">", SIZE=148
    )


phmo_region_permutation_rigid_bodie = Struct("rigid_bodies",
    SInt16("rigid_body_index"),
    ENDIAN=">", SIZE=2
    )


phmo_region_permutation = Struct("permutations",
    string_id_meta("name"),
    reflexive("rigid_bodies", phmo_region_permutation_rigid_bodie),
    ENDIAN=">", SIZE=16
    )


phmo_region = Struct("regions",
    string_id_meta("name"),
    reflexive("permutations", phmo_region_permutation),
    ENDIAN=">", SIZE=16
    )


phmo_node = Struct("nodes",
    string_id_meta("name"),
    Bool16("flags",
        ),
    SInt16("ancestor"),
    SInt16("sibling"),
    SInt16("child"),
    ENDIAN=">", SIZE=12
    )


phmo_limited_hinge_constraint = Struct("limited_hinge_constraints",
    string_id_meta("name"),
    SInt16("node_a"),
    SInt16("node_b"),
    Float("a_scale"),
    Float("a_forward_i"),
    Float("a_forward_j"),
    Float("a_forward_k"),
    Float("a_left_i"),
    Float("a_left_j"),
    Float("a_left_k"),
    Float("a_up_i"),
    Float("a_up_j"),
    Float("a_up_k"),
    Float("a_position_x"),
    Float("a_position_y"),
    Float("a_position_z"),
    Float("b_scale"),
    Float("b_forward_i"),
    Float("b_forward_j"),
    Float("b_forward_k"),
    Float("b_left_i"),
    Float("b_left_j"),
    Float("b_left_k"),
    Float("b_up_i"),
    Float("b_up_j"),
    Float("b_up_k"),
    Float("b_position_x"),
    Float("b_position_y"),
    Float("b_position_z"),
    SInt16("edge_index"),
    SInt16("unknown"),
    Pad(4),
    Float("limit_friction"),
    Float("limit_min_angle"),
    Float("limit_max_angle"),
    ENDIAN=">", SIZE=132
    )


phmo_phantom = Struct("phantoms",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    SEnum16("shape_type", *phmo_list_shape_shape_type),
    SInt16("shape_index"),
    Pad(8),
    SInt32("unknown_3"),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_4"),
    ENDIAN=">", SIZE=44
    )


phmo_meta_def = BlockDef("phmo",
    Pad(4),
    Float("mass"),
    Float("low_frequency_decativation_scale"),
    Float("high_frequency_decativation_scale"),
    Pad(8),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    reflexive("unknown_6", phmo_unknown_6),
    reflexive("unknown_7", phmo_unknown_7),
    reflexive("phantom_types", phmo_phantom_type),
    reflexive("unknown_8", phmo_unknown_8),
    reflexive("node_edges", phmo_node_edge),
    reflexive("rigid_bodies", phmo_rigid_bodie),
    reflexive("materials", phmo_material),
    reflexive("spheres", phmo_sphere),
    Pad(12),
    reflexive("pills", phmo_pill),
    reflexive("boxes", phmo_boxe),
    reflexive("triangles", phmo_triangle),
    reflexive("polyhedra", phmo_polyhedra),
    reflexive("polyhedron_four_vectors", phmo_polyhedron_four_vector),
    reflexive("polyhedron_plane_equations", phmo_polyhedron_plane_equation),
    Pad(12),
    reflexive("lists", phmo_list),
    reflexive("list_shapes", phmo_list_shape),
    reflexive("mopps", phmo_mopp),
    rawdata_ref("mopp_codes"),
    reflexive("hinge_constraints", phmo_hinge_constraint),
    reflexive("ragdoll_constraints", phmo_ragdoll_constraint),
    reflexive("regions", phmo_region),
    reflexive("nodes", phmo_node),
    Pad(24),
    reflexive("limited_hinge_constraints", phmo_limited_hinge_constraint),
    Pad(36),
    reflexive("phantoms", phmo_phantom),
    Pad(8),
    TYPE=Struct, ENDIAN=">", SIZE=416
    )
