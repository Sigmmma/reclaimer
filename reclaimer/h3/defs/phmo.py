#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	Named phmo parts. such as Forge 2.0
# revision: 3		author: Lord Zedd
# 	Messy Messy Messy
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
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


phmo_unknown_2 = Struct("unknown_2",
    h3_string_id("unknown_0"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


phmo_unknown_3 = Struct("unknown_3",
    h3_string_id("name"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=5),
    Pad(8),
    ENDIAN=">", SIZE=32
    )


phmo_phantom_type = Struct("phantom_type",
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
    SInt16("unknown_0", VISIBLE=False),
    h3_string_id("marker_name"),
    h3_string_id("alignment_marker_name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    Float("hooke_s_law_e"),
    Float("linear_dead_radius"),
    Float("center_acceleration"),
    Float("center_max_velocity"),
    Float("axis_acceleration"),
    Float("axis_max_velocity"),
    Float("direction_acceleration"),
    Float("direction_max_velocity"),
    BytesRaw("unknown_2", SIZE=28, VISIBLE=False),
    Float("alignment_hooke_s_law_e"),
    float_rad("alignment_acceleration"),
    float_rad("alignment_max_velocity"),
    BytesRaw("unknown_3", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=104
    )


phmo_unknown_4_unknown_0 = Struct("unknown_0",
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


phmo_unknown_4_unknown_1 = Struct("unknown_1",
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


phmo_unknown_4 = Struct("unknown_4",
    h3_reflexive("unknown_0", phmo_unknown_4_unknown_0),
    h3_reflexive("unknown_1", phmo_unknown_4_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


phmo_node_edge_constraint_unknown_0 = Struct("unknown_0",
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=6, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


phmo_node_edge_constraint_unknown_1 = Struct("unknown_1",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


phmo_node_edge_constraint = Struct("constraint",
    SEnum16("type", *phmo_node_edge_constraint_type),
    SInt16("idx"),
    Bool32("flags", *unknown_flags_32),
    Float("friction"),
    h3_reflexive("unknown_0", phmo_node_edge_constraint_unknown_0),
    h3_reflexive("unknown_1", phmo_node_edge_constraint_unknown_1),
    ENDIAN=">", SIZE=36
    )


phmo_node_edge = Struct("node_edge",
    SInt16("node_a_global_material_index"),
    SInt16("node_b_global_material_index"),
    SInt16("node_a"),
    SInt16("node_b"),
    h3_reflexive("constraints", phmo_node_edge_constraint),
    h3_string_id("node_a_material"),
    h3_string_id("node_b_material"),
    ENDIAN=">", SIZE=28
    )


phmo_rigid_bodie = Struct("rigid_bodie",
    SInt16("node"),
    SInt16("region"),
    SInt16("permutations"),
    SInt16("unknown"),
    QStruct("bounding_sphere_offset", INCLUDE=xyz_float),
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


phmo_material = Struct("material",
    h3_string_id("name"),
    h3_string_id("material_name"),
    SInt16("phantom_type_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=12
    )


phmo_sphere = Struct("sphere",
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_2"),
    Float("radius_0"),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_5"),
    Float("radius_1"),
    BytesRaw("unknown_6", SIZE=12, VISIBLE=False),
    QStruct("translation", INCLUDE=ijk_float),
    Float("translation_radius"),
    ENDIAN=">", SIZE=112
    )


phmo_pill = Struct("pill",
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    QStruct("bottom", INCLUDE=ijk_float),
    Float("bottom_radius"),
    QStruct("top", INCLUDE=ijk_float),
    Float("top_radius"),
    ENDIAN=">", SIZE=96
    )


phmo_boxe = Struct("boxe",
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_2"),
    Float("radius_0", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    QStruct("half_extents", INCLUDE=ijk_float),
    Float("half_extents_radius"),
    SInt32("unknown_4", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_5", VISIBLE=False),
    Float("radius_1"),
    Pad(12),
    QStruct("rotation_i", INCLUDE=ijk_float),
    Float("rotation_i_radius"),
    QStruct("rotation_j", INCLUDE=ijk_float),
    Float("rotation_j_radius"),
    QStruct("rotation_k", INCLUDE=ijk_float),
    Float("rotation_k_radius"),
    QStruct("translation", INCLUDE=ijk_float),
    Float("translation_radius"),
    ENDIAN=">", SIZE=176
    )


phmo_triangle = Struct("triangle",
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    BytesRaw("unknown_3", SIZE=80, VISIBLE=False),
    ENDIAN=">", SIZE=128
    )


phmo_polyhedra = Struct("polyhedra",
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    QStruct("aabb_half_extents", INCLUDE=ijk_float),
    Float("aabb_half_extents_radius"),
    QStruct("aabb_center", INCLUDE=ijk_float),
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


phmo_polyhedron_four_vector = Struct("polyhedron_four_vector",
    QStruct("four_vectors_x", INCLUDE=ijk_float),
    Float("four_vectors_x_radius"),
    QStruct("four_vectors_y", INCLUDE=ijk_float),
    Float("four_vectors_y_radius"),
    QStruct("four_vectors_z", INCLUDE=ijk_float),
    Float("four_vectors_z_radius"),
    ENDIAN=">", SIZE=48
    )


phmo_polyhedron_plane_equation = Struct("polyhedron_plane_equation",
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=4),
    ENDIAN=">", SIZE=16
    )


phmo_list = Struct("list",
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    Pad(12),
    SInt32("child_shapes_size"),
    UInt32("child_shapes_capacity"),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=80
    )


phmo_list_shape = Struct("list_shape",
    SEnum16("shape_type", *phmo_list_shape_shape_type),
    SInt16("shape_index"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    UInt32("unknown_1", VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


phmo_mopp = Struct("mopp",
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    Pad(4),
    SEnum16("shape_type", *phmo_list_shape_shape_type),
    SInt16("shape_index"),
    BytesRaw("unknown_3", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


phmo_hinge_constraint = Struct("hinge_constraint",
    h3_string_id("name"),
    SInt16("node_a"),
    SInt16("node_b"),
    Float("a_scale"),
    QStruct("a_forward", INCLUDE=ijk_float),
    QStruct("a_left", INCLUDE=ijk_float),
    QStruct("a_up", INCLUDE=ijk_float),
    QStruct("a_position", INCLUDE=xyz_float),
    Float("b_scale"),
    QStruct("b_forward", INCLUDE=ijk_float),
    QStruct("b_left", INCLUDE=ijk_float),
    QStruct("b_up", INCLUDE=ijk_float),
    QStruct("b_position", INCLUDE=ijk_float),
    SInt16("edge_index"),
    SInt16("unknown_0"),
    Pad(4),
    ENDIAN=">", SIZE=120
    )


phmo_ragdoll_constraint = Struct("ragdoll_constraint",
    h3_string_id("name"),
    SInt16("node_a"),
    SInt16("node_b"),
    Float("a_scale"),
    QStruct("a_forward", INCLUDE=ijk_float),
    QStruct("a_left", INCLUDE=ijk_float),
    QStruct("a_up", INCLUDE=ijk_float),
    QStruct("a_position", INCLUDE=xyz_float),
    Float("b_scale"),
    QStruct("b_forward", INCLUDE=ijk_float),
    QStruct("b_left", INCLUDE=ijk_float),
    QStruct("b_up", INCLUDE=ijk_float),
    QStruct("b_position", INCLUDE=xyz_float),
    SInt16("edge_index"),
    SInt16("unknown_0"),
    Pad(4),
    QStruct("twist", INCLUDE=from_to),
    QStruct("cone", INCLUDE=from_to),
    QStruct("plane", INCLUDE=from_to),
    Float("max_friction_torque"),
    ENDIAN=">", SIZE=148
    )


phmo_region_permutation_rigid_bodie = Struct("rigid_bodie",
    SInt16("rigid_body_index"),
    ENDIAN=">", SIZE=2
    )


phmo_region_permutation = Struct("permutation",
    h3_string_id("name"),
    h3_reflexive("rigid_bodies", phmo_region_permutation_rigid_bodie),
    ENDIAN=">", SIZE=16
    )


phmo_region = Struct("region",
    h3_string_id("name"),
    h3_reflexive("permutations", phmo_region_permutation),
    ENDIAN=">", SIZE=16
    )


phmo_node = Struct("node",
    h3_string_id("name"),
    Bool16("flags", *unknown_flags_16),
    SInt16("ancestor"),
    SInt16("sibling"),
    SInt16("child"),
    ENDIAN=">", SIZE=12
    )


phmo_limited_hinge_constraint = Struct("limited_hinge_constraint",
    h3_string_id("name"),
    SInt16("node_a"),
    SInt16("node_b"),
    Float("a_scale"),
    QStruct("a_forward", INCLUDE=ijk_float),
    QStruct("a_left", INCLUDE=ijk_float),
    QStruct("a_up", INCLUDE=ijk_float),
    QStruct("a_position", INCLUDE=xyz_float),
    Float("b_scale"),
    QStruct("b_forward", INCLUDE=ijk_float),
    QStruct("b_left", INCLUDE=ijk_float),
    QStruct("b_up", INCLUDE=ijk_float),
    QStruct("b_position", INCLUDE=xyz_float),
    SInt16("edge_index"),
    SInt16("unknown_0"),
    Pad(4),
    Float("limit_friction"),
    Float("limit_min_angle"),
    Float("limit_max_angle"),
    ENDIAN=">", SIZE=132
    )


phmo_phantom = Struct("phantom",
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_1"),
    SEnum16("shape_type", *phmo_list_shape_shape_type),
    SInt16("shape_index"),
    Pad(8),
    SInt32("unknown_3", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_4"),
    ENDIAN=">", SIZE=44
    )


phmo_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("mass"),
    Float("low_frequency_decativation_scale"),
    Float("high_frequency_decativation_scale"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_2", phmo_unknown_2),
    h3_reflexive("unknown_3", phmo_unknown_3),
    h3_reflexive("phantom_types", phmo_phantom_type),
    h3_reflexive("unknown_4", phmo_unknown_4),
    h3_reflexive("node_edges", phmo_node_edge),
    h3_reflexive("rigid_bodies", phmo_rigid_bodie),
    h3_reflexive("materials", phmo_material),
    h3_reflexive("spheres", phmo_sphere),
    BytesRaw("multi_spheres_block_here", SIZE=12, VISIBLE=False),
    h3_reflexive("pills", phmo_pill),
    h3_reflexive("boxes", phmo_boxe),
    h3_reflexive("triangles", phmo_triangle),
    h3_reflexive("polyhedra", phmo_polyhedra),
    h3_reflexive("polyhedron_four_vectors", phmo_polyhedron_four_vector),
    h3_reflexive("polyhedron_plane_equations", phmo_polyhedron_plane_equation),
    BytesRaw("mass_distributions_block_here", SIZE=12, VISIBLE=False),
    h3_reflexive("lists", phmo_list),
    h3_reflexive("list_shapes", phmo_list_shape),
    h3_reflexive("mopps", phmo_mopp),
    h3_rawdata_ref("mopp_codes"),
    h3_reflexive("hinge_constraints", phmo_hinge_constraint),
    h3_reflexive("ragdoll_constraints", phmo_ragdoll_constraint),
    h3_reflexive("regions", phmo_region),
    h3_reflexive("nodes", phmo_node),
    BytesRaw("unknown_5", SIZE=24, VISIBLE=False),
    h3_reflexive("limited_hinge_constraints", phmo_limited_hinge_constraint),
    BytesRaw("ball_and_socket_constraint_block", SIZE=36, VISIBLE=False),
    h3_reflexive("phantoms", phmo_phantom),
    BytesRaw("unknown_6", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=416
    )


def get():
    return phmo_def

phmo_def = TagDef("phmo",
    h3_blam_header('phmo'),
    phmo_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["phmo"], endian=">", tag_cls=H3Tag
    )
