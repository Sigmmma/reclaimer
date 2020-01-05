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
# revision: 2		author: -DeToX-
# 	Named Some Values...
# revision: 3		author: Halodu03de
# 	added chunk code
# revision: 4		author: Lord Zedd
# 	Lots of updates
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

hlmt_model_object_data_type = (
    "not_set",
    "user_defined",
    "auto_generated",
    )

hlmt_new_damage_info_damage_section_instant_response_constraint_damage_type = (
    "none",
    "destroy_one_of_group",
    "destroy_entire_group",
    "loosen_one_of_group",
    "loosen_entire_group",
    )

hlmt_new_damage_info_damage_section_instant_response_response_type = (
    "recieves_all_damage",
    "recieves_area_effect_damage",
    "recieves_local_damage",
    )

hlmt_new_damage_info_damage_section_instant_response_unknown_special_damage = (
    "none",
    "_1",
    "_2",
    "_3",
    )

hlmt_variant_region_sort_order = (
    "no_sorting",
    "neg_5_closest",
    "neg_4",
    "neg_3",
    "neg_2",
    "neg_1",
    "_0_same_as_model",
    "_1",
    "_2",
    "_3",
    "_4",
    "_5_farthest",
    )


hlmt_variant_region_permutation_state = Struct("state",
    h3_string_id("name"),
    SInt8("model_permutation_index"),
    Bool8("property_flags",
        "blurred",
        "hella_blurred",
        "shielded",
        ),
    SEnum16("state", *vehi_friction_point_model_state_destroyed),
    h3_dependency("looping_effect"),
    h3_string_id("looping_effect_marker_name"),
    Float("initial_probability"),
    ENDIAN=">", SIZE=32
    )


hlmt_variant_region_permutation = Struct("permutation",
    h3_string_id("name"),
    SInt8("model_permutation_index"),
    Bool8("flags",
        "copy_states_to_all_permutations",
        ),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    Float("probability"),
    h3_reflexive("states", hlmt_variant_region_permutation_state),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


hlmt_variant_region = Struct("region",
    h3_string_id("name"),
    SInt8("model_region_index"),
    SInt8("unknown", VISIBLE=False),
    SInt16("parent_variant_index"),
    h3_reflexive("permutations", hlmt_variant_region_permutation),
    SEnum32("sort_order", *hlmt_variant_region_sort_order),
    ENDIAN=">", SIZE=24
    )


hlmt_variant_object = Struct("object",
    h3_string_id("parent_marker"),
    h3_string_id("child_marker"),
    h3_string_id("child_variant"),
    h3_dependency("child_object"),
    ENDIAN=">", SIZE=28
    )


hlmt_variant = Struct("variant",
    h3_string_id("name"),
    Array("model_region_index_array", SUB_STRUCT=SInt8("model_region_index"), SIZE=16),
    h3_reflexive("regions", hlmt_variant_region),
    h3_reflexive("objects", hlmt_variant_object),
    SInt32("instance_group_index"),
    BytesRaw("unknown", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=56
    )


hlmt_instance_group_instance_member = Struct("instance_member",
    SInt32("unknown", VISIBLE=False),
    h3_string_id("instance_name"),
    Float("probability"),
    Bool32("instance_flags_1", *("instance_%s" % i for i in range(32))),
    Bool32("instance_flags_2", *("instance_%s" % i for i in range(32, 64))),
    ENDIAN=">", SIZE=20
    )


hlmt_instance_group = Struct("instance_group",
    h3_string_id("name"),
    SInt32("unknown", VISIBLE=False),
    h3_reflexive("instance_members", hlmt_instance_group_instance_member),
    Float("probability"),
    ENDIAN=">", SIZE=24
    )


hlmt_material = Struct("material",
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("damage_section_index"),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("material_name"),
    SInt16("global_material_index"),
    SInt16("unknown_3", VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


hlmt_new_damage_info_damage_section_instant_response = Struct("instant_response",
    SEnum16("response_type", *hlmt_new_damage_info_damage_section_instant_response_response_type),
    SEnum16("constraint_damage_type", *hlmt_new_damage_info_damage_section_instant_response_constraint_damage_type),
    h3_string_id("trigger"),
    Bool32("flags",
        "kills_object",
        "inhibits_melee_attack",
        "inhibits_weapon_attack",
        "inhibits_walking",
        "forces_drop_weapon",
        "kills_weapon_primary_trigger",
        "kills_weapon_secondary_trigger",
        "destroys_object",
        "damages_weapon_primary_trigger",
        "damages_weapon_secondary_trigger",
        "light_damage_left_turn",
        "major_damage_left_turn",
        "light_damage_right_turn",
        "major_damage_right_turn",
        "light_damage_engine",
        "major_damage_engine",
        "kills_object_no_player_solo",
        "causes_detonation",
        "destroy_all_group_constraints",
        "kills_variant_objects",
        "force_unattached_effects",
        "fires_under_threshold",
        "triggers_special_death",
        "only_on_special_death",
        "only_not_on_special_death",
        ("causes_detonation_in_single_player", 1 << 26),
        ),
    Float("damage_threshold"),
    h3_dependency("primary_transition_effect"),
    h3_dependency("secondary_transition_effect"),
    h3_dependency("transition_damage_effect"),
    h3_string_id("region"),
    SEnum16("new_state", *vehi_friction_point_model_state_destroyed),
    SInt16("runtime_region_index"),
    h3_string_id("secondary_region"),
    SEnum16("secondary_new_state", *vehi_friction_point_model_state_destroyed),
    SInt16("secondary_runtime_region_index"),
    SInt16("unknown"),
    SEnum16("unknown_special_damage", *hlmt_new_damage_info_damage_section_instant_response_unknown_special_damage),
    h3_string_id("special_damage_case"),
    h3_string_id("effect_marker_name"),
    h3_string_id("damage_effect_marker_name"),
    Float("response_delay"),
    h3_dependency("delay_effect"),
    h3_string_id("delay_effect_marker_name"),
    h3_string_id("ejecting_seat_label"),
    Float("skip_fraction"),
    h3_string_id("destroyed_child_object_marker_name"),
    Float("total_damage_threshold"),
    ENDIAN=">", SIZE=136
    )


hlmt_new_damage_info_damage_section = Struct("damage_section",
    h3_string_id("name"),
    Bool32("flags",
        "absorbs_body_damage",
        "takes_full_damage_when_object_dies",
        "cannot_die_with_riders",
        "takes_full_damage_when_object_destroyed",
        "restored_on_ressurection",
        ("headshotable", 1 << 7),
        "ignores_shields",
        ),
    Float("vitality_percentage"),
    h3_reflexive("instant_responses", hlmt_new_damage_info_damage_section_instant_response),
    BytesRaw("unknown_0", SIZE=24, VISIBLE=False),
    Float("stun_time"),
    Float("recharge_time"),
    Float("unknown_1", VISIBLE=False),
    h3_string_id("resurrection_region_name"),
    SInt16("ressurection_region_runtime_index"),
    SInt16("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=68
    )


hlmt_new_damage_info_node = Struct("node",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


hlmt_new_damage_info_damage_seat_unknown = Struct("unknown",
    h3_string_id("node"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=36, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=44
    )


hlmt_new_damage_info_damage_seat = Struct("damage_seat",
    h3_string_id("seat_label"),
    Float("direct_damage_scale"),
    Float("damage_transfer_fall_off_radius"),
    Float("maximum_transfer_damage_scale"),
    Float("minimum_transfer_damage_scale"),
    h3_reflexive("unknown", hlmt_new_damage_info_damage_seat_unknown),
    ENDIAN=">", SIZE=32
    )


hlmt_new_damage_info_damage_constraint = Struct("damage_constraint",
    h3_string_id("physics_model_constraint_name"),
    h3_string_id("damage_constraint_name"),
    h3_string_id("damage_constraint_group_name"),
    Float("group_probability_scale"),
    SEnum16("type", *phmo_node_edge_constraint_type),
    SInt16("idx"),
    ENDIAN=">", SIZE=20
    )


hlmt_new_damage_info = Struct("new_damage_info",
    Bool32("flags",
        "takes_shield_damage_for_children",
        "takes_body_damage_for_children",
        "always_shields_friendly_damage",
        "passes_area_damage_to_children",
        "parent_never_takes_body_damage_for_children",
        "only_damaged_by_explosives",
        "parent_never_takes_shield_damage_for_children",
        "cannot_die_from_damage",
        "passes_attached_damage_to_riders",
        ("only_damaged_by_player", 1 << 11),
        ),
    h3_string_id("global_indirect_material_name"),
    SInt16("indirect_damage_section"),
    SInt16("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SEnum8("collision_damage_reporting_type", *proj_damage_reporting_type),
    SEnum8("response_damage_reporting_type", *proj_damage_reporting_type),
    SInt16("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=20, VISIBLE=False),
    Float("maximum_vitality"),
    Float("minimum_stun_damage_0"),
    Float("stun_time_0"),
    Float("recharge_time"),
    Float("recharge_fraction"),
    Pad(64),
    Float("maximum_shield_vitality"),
    h3_string_id("global_shield_material_name"),
    Float("minimum_stun_damage_1"),
    Float("stun_time_1"),
    Float("shield_recharge_time"),
    Float("shield_damaged_threshold"),
    h3_dependency("shield_damaged_effect"),
    h3_dependency("shield_depleted_effect"),
    h3_dependency("shield_recharging_effect"),
    h3_reflexive("damage_sections", hlmt_new_damage_info_damage_section),
    h3_reflexive("nodes", hlmt_new_damage_info_node),
    SInt16("global_shield_material_index"),
    SInt16("global_indirect_material_index"),
    Float("unknown_5", VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    h3_reflexive("damage_seats", hlmt_new_damage_info_damage_seat),
    h3_reflexive("damage_constraints", hlmt_new_damage_info_damage_constraint),
    ENDIAN=">", SIZE=256
    )


hlmt_target = Struct("target",
    h3_string_id("marker_name"),
    Float("size"),
    float_rad("cone_angle", VISIBLE=False),
    SInt16("damage_section"),
    SInt16("variant"),
    Float("targeting_relevance"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    Bool32("flags",
        "locked_by_human_tracking",
        "locked_by_plasma_tracking",
        "headshot",
        ("vulnerable", 1 << 4),
        ("always_locked_by_plasma_tracking", 1 << 6),
        ),
    Float("lock_on_distance"),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


hlmt_collision_region_permutation = Struct("permutation",
    h3_string_id("name"),
    Bool8("flags",
        "cannot_be_chosen_randomly",
        ),
    SInt8("collision_permutation_index"),
    SInt8("physics_permutation_index"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


hlmt_collision_region = Struct("collision_region",
    h3_string_id("name"),
    SInt8("collision_region_index"),
    SInt8("physics_region_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    h3_reflexive("permutations", hlmt_collision_region_permutation),
    ENDIAN=">", SIZE=20
    )


hlmt_node = Struct("node",
    h3_string_id("name"),
    SInt16("parent_node"),
    SInt16("first_child_node"),
    SInt16("next_sibling_node"),
    SInt16("import_node_index"),
    QStruct("default_translation", INCLUDE=xyz_float),
    QStruct("default_rotation", INCLUDE=ijkw_float),
    Float("default_scale"),
    QStruct("inverse_forward", INCLUDE=ijk_float),
    QStruct("inverse_left", INCLUDE=ijk_float),
    QStruct("inverse_up", INCLUDE=ijk_float),
    QStruct("inverse_position", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=92
    )


hlmt_model_object_data = Struct("model_object_data",
    SEnum16("type", *hlmt_model_object_data_type),
    SInt16("unknown", VISIBLE=False),
    QStruct("offset", INCLUDE=xyz_float),
    Float("radius"),
    ENDIAN=">", SIZE=20
    )


hlmt_unknown_3 = Struct("unknown_3",
    h3_string_id("region"),
    h3_string_id("permutation"),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


hlmt_unknown_4 = Struct("unknown_4",
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


hlmt_unknown_5 = Struct("unknown_5",
    h3_string_id("marker_0", VISIBLE=False),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_string_id("marker_1", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


hlmt_body = Struct("tagdata",
    h3_dependency("model"),
    h3_dependency("collision_model"),
    h3_dependency("animation"),
    h3_dependency("physics_model"),
    Float("reduce_to_l1_super_low"),
    Float("reduce_to_l2_low"),
    Float("reduce_to_l3_medium"),
    Float("reduce_to_l4_high"),
    Float("reduce_to_l5_super_high"),
    h3_dependency("lod_model"),
    h3_reflexive("variants", hlmt_variant),
    h3_reflexive("instance_groups", hlmt_instance_group),
    h3_reflexive("materials", hlmt_material),
    h3_reflexive("new_damage_info", hlmt_new_damage_info),
    h3_reflexive("targets", hlmt_target),
    h3_reflexive("collision_regions", hlmt_collision_region),
    h3_reflexive("nodes", hlmt_node),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("model_object_data", hlmt_model_object_data),
    h3_dependency("primary_dialog"),
    h3_dependency("secondary_dialog"),
    Bool32("flags",
        "active_camo_always_on",
        "active_camo_always_merge",
        "active_camo_never_merge",
        ),
    h3_string_id("default_dialogue_effect"),
    Bool32("render_only_node_flags_1", *("node_%s" % i for i in range(32)), VISIBLE=False),
    Bool32("render_only_node_flags_2", *("node_%s" % i for i in range(32, 64)), VISIBLE=False),
    Bool32("render_only_node_flags_3", *("node_%s" % i for i in range(64, 96)), VISIBLE=False),
    Bool32("render_only_node_flags_4", *("node_%s" % i for i in range(96, 128)), VISIBLE=False),
    Bool32("render_only_node_flags_5", *("node_%s" % i for i in range(128, 160)), VISIBLE=False),
    Bool32("render_only_node_flags_6", *("node_%s" % i for i in range(160, 192)), VISIBLE=False),
    Bool32("render_only_node_flags_7", *("node_%s" % i for i in range(192, 224)), VISIBLE=False),
    Bool32("render_only_node_flags_8", *("node_%s" % i for i in range(224, 256)), VISIBLE=False),
    Bool32("render_only_section_flags_1", *("section_%s" % i for i in range(32)), VISIBLE=False),
    Bool32("render_only_section_flags_2", *("section_%s" % i for i in range(32, 64)), VISIBLE=False),
    Bool32("render_only_section_flags_3", *("section_%s" % i for i in range(64, 96)), VISIBLE=False),
    Bool32("render_only_section_flags_4", *("section_%s" % i for i in range(96, 128)), VISIBLE=False),
    Bool32("render_only_section_flags_5", *("section_%s" % i for i in range(128, 160)), VISIBLE=False),
    Bool32("render_only_section_flags_6", *("section_%s" % i for i in range(160, 192)), VISIBLE=False),
    Bool32("render_only_section_flags_7", *("section_%s" % i for i in range(192, 224)), VISIBLE=False),
    Bool32("render_only_section_flags_8", *("section_%s" % i for i in range(224, 256)), VISIBLE=False),
    Bool32("runtime_flags",
        "contains_runtime_nodes",
        VISIBLE=False,
        ),
    BytesRaw("scenario_load_parameters_block", SIZE=12, VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    h3_reflexive("unknown_3", hlmt_unknown_3),
    h3_reflexive("unknown_4", hlmt_unknown_4),
    h3_reflexive("unknown_5", hlmt_unknown_5),
    h3_dependency("shield_impact_third_person"),
    h3_dependency("shield_impact_first_person"),
    ENDIAN=">", SIZE=392
    )


def get():
    return hlmt_def

hlmt_def = TagDef("hlmt",
    h3_blam_header('hlmt'),
    hlmt_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["hlmt"], endian=">", tag_cls=H3Tag
    )
