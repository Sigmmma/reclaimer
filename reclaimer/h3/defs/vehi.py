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
# 	Named some values...
# revision: 3		author: Veegie
# 	Named most values...
# revision: 4		author: -DeToX-
# 	Removed Veegie's garbage values, fixed seats reflexive and added seats intraflexives.
# revision: 5		author: DeadCanadian
# 	Named types
# revision: 6		author: Lord Zedd
# 	Portin'
# revision: 7		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

vehi_friction_point_friction_type = (
    "point",
    "forward",
    )

vehi_player_training_vehicle_type = (
    "none",
    "warthog",
    "warthog_turret",
    "ghost",
    "banshee",
    "tank",
    "wraith",
    )

vehi_vehicle_size = (
    "small",
    "large",
    )


vehi_early_mover_propertie = Struct("early_mover_propertie",
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


vehi_ai_propertie = Struct("ai_propertie",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    h3_string_id("ai_type_name"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    SEnum16("size", *bloc_ai_propertie_size),
    SEnum16("leap_jump_speed", *bloc_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


vehi_function = Struct("function",
    Bool32("flags",
        "invert",
        "mapping_does_not_controls_active",
        "always_active",
        "random_time_offset",
        ),
    h3_string_id("import_name"),
    h3_string_id("export_name"),
    h3_string_id("turn_off_with"),
    Float("minimum_value"),
    h3_rawdata_ref("default_function"),
    h3_string_id("scale_by"),
    ENDIAN=">", SIZE=44
    )


vehi_attachment = Struct("attachment",
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


vehi_widget = Struct("widget",
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


vehi_change_color_initial_permutation = Struct("initial_permutation",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


vehi_change_color_function = Struct("function",
    Bool32("scale_flags",
        "blend_in_hsv",
        "more_colors",
        ),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("darken_by"),
    h3_string_id("scale_by"),
    ENDIAN=">", SIZE=32
    )


vehi_change_color = Struct("change_color",
    h3_reflexive("initial_permutations", vehi_change_color_initial_permutation),
    h3_reflexive("functions", vehi_change_color_function),
    ENDIAN=">", SIZE=24
    )


vehi_predicted_resource = Struct("predicted_resource",
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


vehi_multiplayer_object_propertie = Struct("multiplayer_object_propertie",
    Bool16("engine_flags",
        "capture_the_flag",
        "slayer",
        "oddball",
        "king_of_the_hill",
        "juggernaut",
        "territories",
        "assault",
        "vip",
        "infection",
        ),
    SEnum8("object_type", *bloc_multiplayer_object_propertie_object_type),
    Bool8("teleporter_flags",
        "disallows_players",
        "allows_land_vehicles",
        "allows_heavy_vehicles",
        "allows_flying_vehicles",
        "allows_projectiles",
        ),
    Bool16("flags",
        "editor_only",
        ),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *bloc_multiplayer_object_propertie_spawn_timer_mode),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    Float("radius_width"),
    Float("length"),
    Float("top"),
    Float("bottom"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    SInt32("unknown_3", VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    h3_dependency("child_object"),
    SInt32("unknown_5"),
    h3_dependency("shape_shader"),
    h3_dependency("unknown_shader"),
    h3_dependency("unknown_6"),
    h3_dependency("unknown_7"),
    h3_dependency("unknown_8"),
    h3_dependency("unknown_9"),
    h3_dependency("unknown_10"),
    h3_dependency("unknown_11"),
    ENDIAN=">", SIZE=196
    )


vehi_metagame_propertie = Struct("metagame_propertie",
    Bool8("flags",
        "must_have_active_seats",
        ),
    SEnum8("unit", *bloc_metagame_propertie_unit),
    SEnum8("classification", *bloc_metagame_propertie_classification),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("points"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


vehi_camera_track = Struct("camera_track",
    h3_dependency("track"),
    ENDIAN=">", SIZE=16
    )


vehi_unknown_7 = Struct("unknown_7",
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=19, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=76
    )


vehi_posture = Struct("posture",
    h3_string_id("name"),
    QStruct("pill_offset", INCLUDE=ijk_float),
    ENDIAN=">", SIZE=16
    )


vehi_hud_interface = Struct("hud_interface",
    h3_dependency("unit_hud_interface"),
    ENDIAN=">", SIZE=16
    )


vehi_dialogue_variant = Struct("dialogue_variant",
    SInt16("variant_number"),
    SInt16("unknown", VISIBLE=False),
    h3_dependency("dialogue"),
    ENDIAN=">", SIZE=20
    )


vehi_powered_seat = Struct("powered_seat",
    Float("driver_powerup_time"),
    Float("driver_powerdown_time"),
    ENDIAN=">", SIZE=8
    )


vehi_weapon = Struct("weapon",
    h3_dependency("weapon"),
    ENDIAN=">", SIZE=16
    )


vehi_seat_camera_track = Struct("camera_track",
    h3_dependency("track"),
    ENDIAN=">", SIZE=16
    )


vehi_seat_unknown_6 = Struct("unknown_6",
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=19, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=76
    )


vehi_seat_unit_hud_interface = Struct("unit_hud_interface",
    h3_dependency("unit_hud_interface"),
    ENDIAN=">", SIZE=16
    )


vehi_seat = Struct("seat",
    Bool32("flags",
        "invisible",
        "locked",
        "driver",
        "gunner",
        "third_person_camera",
        "allows_weapons",
        "third_person_on_enter",
        "first_person_camera_slaved_to_gun",
        "allow_vehicle_communication_animations",
        "not_valid_without_driver",
        "allow_ai_noncombatants",
        "boarding_seat",
        "ai_firing_disabled_by_max_acceleration",
        "boarding_enters_seat",
        "boarding_need_any_passenger",
        "controls_open_and_close",
        "invalid_for_player",
        "invalid_for_non_player",
        "gunner_player_only",
        "invisible_under_major_damage",
        ("detachable_weapon", 1 << 22),
        ),
    h3_string_id("seat_animation"),
    h3_string_id("seat_marker_name"),
    h3_string_id("entry_marker_s_name"),
    h3_string_id("boarding_grenade_marker"),
    h3_string_id("boarding_grenade_string"),
    h3_string_id("boarding_melee_string"),
    h3_string_id("detach_weapon_string"),
    Float("ping_scale"),
    Float("turnover_time"),
    QStruct("acceleration_range", INCLUDE=ijk_float),
    Float("acceleration_action_scale"),
    Float("acceleration_attach_scale"),
    Float("ai_scariness"),
    SEnum16("ai_seat_type", *gint_seat_ai_seat_type),
    SInt16("boarding_seat"),
    Float("listener_interpolation_factor"),
    QStruct("yaw_rate_bounds", INCLUDE=from_to),
    QStruct("pitch_rate_bounds", INCLUDE=from_to),
    Float("unknown_0", VISIBLE=False),
    QStruct("speed_reference", INCLUDE=from_to),
    Float("speed_exponent"),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("camera_marker_name"),
    h3_string_id("camera_submerged_marker_name"),
    float_rad("pitch_auto_level"),
    from_to_rad("pitch_range"),
    h3_reflexive("camera_tracks", vehi_seat_camera_track),
    float_rad("unknown_3", VISIBLE=False),
    float_rad("unknown_4", VISIBLE=False),
    float_rad("unknown_5", VISIBLE=False),
    h3_reflexive("unknown_6", vehi_seat_unknown_6),
    h3_reflexive("unit_hud_interface", vehi_seat_unit_hud_interface),
    h3_string_id("enter_seat_string"),
    from_to_rad("yaw_range"),
    h3_dependency("built_in_gunner"),
    Float("entry_radius"),
    float_rad("entry_marker_cone_angle"),
    float_rad("entry_marker_facing_angle"),
    Float("maximum_relative_velocity"),
    h3_string_id("invisible_seat_region"),
    SInt32("runtime_invisible_seat_region_index"),
    ENDIAN=">", SIZE=228
    )


vehi_tank_engine_motion_propertie_gear = Struct("gear",
    QStruct("torque_0", INCLUDE=from_to),
    Float("peak_torque_scale_0"),
    Float("past_peak_torque_exponent_0"),
    Float("torque_at_max_angular_velovity_0"),
    Float("torque_at_2x_max_angular_velocity_0"),
    QStruct("torque_1", INCLUDE=from_to),
    Float("peak_torque_scale_1"),
    Float("past_peak_torque_exponent_1"),
    Float("torque_at_max_angular_velovity_1"),
    Float("torque_at_2x_max_angular_velocity_1"),
    Float("min_time_to_upshift"),
    Float("engine_upshift_scale"),
    Float("gear_ratio"),
    Float("min_time_to_downshift"),
    Float("engine_downshift_scale"),
    ENDIAN=">", SIZE=68
    )


vehi_tank_engine_motion_propertie = Struct("tank_engine_motion_propertie",
    float_rad("steering_overdampen_cusp_angle"),
    Float("steering_overdamen_exponent"),
    Float("unknown_0"),
    Float("speed_left"),
    Float("speed_right"),
    Float("turning_speed_left"),
    Float("turning_speed_right"),
    Float("speed_left_2"),
    Float("speed_right_2"),
    Float("turning_speed_left_2"),
    Float("turning_speed_right_2"),
    Float("engine_momentum"),
    Float("engine_maximum_angular_velocity"),
    h3_reflexive("gears", vehi_tank_engine_motion_propertie_gear),
    h3_dependency("change_gear_sound"),
    Float("unknown_1"),
    Float("unknown_2"),
    ENDIAN=">", SIZE=88
    )


vehi_engine_motion_propertie_gear = Struct("gear",
    QStruct("torque_0", INCLUDE=from_to),
    Float("peak_torque_scale_0"),
    Float("past_peak_torque_exponent_0"),
    Float("torque_at_max_angular_velovity_0"),
    Float("torque_at_2x_max_angular_velocity_0"),
    QStruct("torque_1", INCLUDE=from_to),
    Float("peak_torque_scale_1"),
    Float("past_peak_torque_exponent_1"),
    Float("torque_at_max_angular_velovity_1"),
    Float("torque_at_2x_max_angular_velocity_1"),
    Float("min_time_to_upshift"),
    Float("engine_upshift_scale"),
    Float("gear_ratio"),
    Float("min_time_to_downshift"),
    Float("engine_downshift_scale"),
    ENDIAN=">", SIZE=68
    )


vehi_engine_motion_propertie = Struct("engine_motion_propertie",
    float_rad("steering_overdampen_cusp_angle"),
    Float("steering_overdamen_exponent"),
    float_rad("maximum_left_turn"),
    float_rad("maximum_right_turn_negative"),
    float_rad("turn_rate"),
    Float("engine_momentum"),
    Float("engine_maximum_angular_velocity"),
    h3_reflexive("gears", vehi_engine_motion_propertie_gear),
    h3_dependency("change_gear_sound"),
    Float("unknown_0"),
    Float("unknown_1"),
    ENDIAN=">", SIZE=64
    )


vehi_dropship_motion_propertie = Struct("dropship_motion_propertie",
    Float("forward_acceleration"),
    Float("backward_acceleration"),
    Float("unknown_0"),
    Float("unknown_1"),
    Float("left_strafe_acceleration"),
    Float("right_strafe_acceleration"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("lift_acceleration"),
    Float("drop_acceleration"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=6),
    float_rad("unknown_4"),
    Float("unknown_5"),
    float_rad("unknown_6"),
    ENDIAN=">", SIZE=76
    )


vehi_antigravity_motion_propertie = Struct("antigravity_motion_propertie",
    float_rad("steering_overdampen_cusp_angle"),
    Float("steering_overdamen_exponent"),
    Float("maximum_forward_speed"),
    Float("maximum_reverse_speed"),
    Float("speed_acceleration"),
    Float("speed_deceleration"),
    Float("maximum_left_slide"),
    Float("maximum_right_slide"),
    Float("slide_acceleration"),
    Float("slide_deceleration"),
    Array("unknown_array_0", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    Float("traction"),
    Pad(4),
    Float("turning_rate"),
    h3_string_id("unknown_1"),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=4),
    h3_string_id("unknown_2"),
    Array("unknown_array_2", SUB_STRUCT=Float("unknown"), SIZE=7),
    float_rad("unknown_3"),
    ENDIAN=">", SIZE=112
    )


vehi_jet_engine_motion_propertie = Struct("jet_engine_motion_propertie",
    float_rad("steering_overdampen_cusp_angle"),
    Float("steering_overdamen_exponent"),
    float_rad("maximum_left_turn"),
    float_rad("maximum_right_turn_negative"),
    float_rad("turn_rate"),
    Float("flying_speed"),
    Float("acceleration"),
    Float("speed_acceleration"),
    Float("speed_deceleration"),
    Float("pitch_left_speed"),
    Float("pitch_right_speed"),
    Float("pitch_rate"),
    Float("unpitch_rate"),
    Float("flight_stability"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("nose_angle"),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    Float("falling_speed"),
    Float("falling_speed_2"),
    Float("unknown_4", VISIBLE=False),
    Float("unknown_5"),
    Float("idle_rise"),
    Float("idle_forward"),
    ENDIAN=">", SIZE=100
    )


vehi_turret_propertie = Struct("turret_propertie",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


vehi_helicopter_motion_propertie = Struct("helicopter_motion_propertie",
    float_rad("maximum_left_turn"),
    float_rad("maximum_right_turn_negative"),
    float_rad("unknown_0"),
    h3_string_id("thrust_front_left"),
    h3_string_id("thrust_front_right"),
    h3_string_id("thrust"),
    Array("unknown_array_0", SUB_STRUCT=float_rad("unknown"), SIZE=4),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=15),
    float_rad("unknown_1"),
    float_rad("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    ENDIAN=">", SIZE=116
    )


vehi_antigravity_engine_motion_propertie_gear = Struct("gear",
    QStruct("torque_0", INCLUDE=from_to),
    Float("peak_torque_scale_0"),
    Float("past_peak_torque_exponent_0"),
    Float("torque_at_max_angular_velovity_0"),
    Float("torque_at_2x_max_angular_velocity_0"),
    QStruct("torque_1", INCLUDE=from_to),
    Float("peak_torque_scale_1"),
    Float("past_peak_torque_exponent_1"),
    Float("torque_at_max_angular_velovity_1"),
    Float("torque_at_2x_max_angular_velocity_1"),
    Float("min_time_to_upshift"),
    Float("engine_upshift_scale"),
    Float("gear_ratio"),
    Float("min_time_to_downshift"),
    Float("engine_downshift_scale"),
    ENDIAN=">", SIZE=68
    )


vehi_antigravity_engine_motion_propertie = Struct("antigravity_engine_motion_propertie",
    float_rad("steering_overdampen_cusp_angle"),
    Float("steering_overdamen_exponent"),
    float_rad("maximum_left_turn"),
    float_rad("maximum_right_turn_negative"),
    float_rad("turn_rate"),
    Float("engine_momentum"),
    Float("engine_maximum_angular_velocity"),
    h3_reflexive("gears", vehi_antigravity_engine_motion_propertie_gear),
    h3_dependency("change_gear_sound"),
    Float("unknown_0"),
    h3_string_id("unknown_1"),
    Array("unknown_array_0", SUB_STRUCT=Float("unknown"), SIZE=6),
    float_rad("unknown_2"),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=5),
    ENDIAN=">", SIZE=112
    )


vehi_autoturret_equipment = Struct("autoturret_equipment",
    float_rad("unknown_0"),
    Float("unknown_1"),
    Pad(12),
    Float("unknown_3"),
    Pad(12),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    ENDIAN=">", SIZE=48
    )


vehi_anti_gravity_point = Struct("anti_gravity_point",
    h3_string_id("marker_name"),
    Bool32("flags",
        "gets_damage_from_region",
        ),
    Float("antigrav_strength"),
    Float("antigrav_offset"),
    Float("antigrav_height"),
    Float("antigrav_dump_factor"),
    Float("antigrav_normal_k1"),
    Float("antigrav_normal_k0"),
    Float("radius"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("damage_source_region_index"),
    h3_string_id("damage_source_region_name"),
    Float("default_state_error"),
    Float("minor_damage_error"),
    Float("medium_damage_error"),
    Float("major_damage_error"),
    Float("destroyed_state_error"),
    ENDIAN=">", SIZE=76
    )


vehi_friction_point = Struct("friction_point",
    h3_string_id("marker_name"),
    Bool32("flags",
        "gets_damage_from_region",
        "powered",
        "front_turning",
        "rear_turning",
        "attached_to_e_brake",
        "can_be_destroyed",
        ),
    Float("fraction_of_total_mass"),
    Float("radius"),
    Float("damaged_radius"),
    SEnum16("friction_type", *vehi_friction_point_friction_type),
    SInt16("unknown_0", VISIBLE=False),
    Float("moving_friction_velocity_diff"),
    Float("e_brake_moving_friction"),
    Float("e_brake_friction"),
    Float("e_brake_moving_friction_velocity_diff"),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("collision_material_name"),
    SInt16("collision_global_material_index"),
    SEnum16("model_state_destroyed", *vehi_friction_point_model_state_destroyed),
    h3_string_id("region_name"),
    SInt32("region_index"),
    ENDIAN=">", SIZE=76
    )


vehi_phantom_shape = Struct("phantom_shape",
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("overall_shape_index_0"),
    SInt32("offset_0"),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=16, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=7),
    BytesRaw("unknown_4", SIZE=4, VISIBLE=False),
    SInt32("multisphere_count"),
    Bool32("flags",
        "has_aabb_phantom",
        ),
    Float("x0"),
    Float("x1"),
    Float("y0"),
    Float("y1"),
    Float("z0"),
    Float("z1"),
    SInt32("unknown_5", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("overall_shape_index_1"),
    SInt32("offset_1"),
    SInt32("number_of_spheres_0"),
    BytesRaw("unknown_6", SIZE=140, VISIBLE=False),
    SInt32("unknown_7", VISIBLE=False),
    SInt16("size_4"),
    SInt16("size_5"),
    SInt32("overall_shape_index_2"),
    SInt32("offset_2"),
    SInt32("number_of_spheres_1"),
    BytesRaw("unknown_8", SIZE=140, VISIBLE=False),
    SInt32("unknown_9", VISIBLE=False),
    SInt16("size_6"),
    SInt16("size_7"),
    SInt32("overall_shape_index_3"),
    SInt32("offset_3"),
    SInt32("number_of_spheres_2"),
    BytesRaw("unknown_10", SIZE=140, VISIBLE=False),
    SInt32("unknown_11", VISIBLE=False),
    SInt16("size_8"),
    SInt16("size_9"),
    SInt32("overall_shape_index_4"),
    SInt32("offset_4"),
    SInt32("number_of_spheres_3"),
    BytesRaw("unknown_12", SIZE=204, VISIBLE=False),
    ENDIAN=">", SIZE=816
    )


vehi_body = Struct("tagdata",
    SEnum16("object_type", *bloc_object_type),
    Bool16("flags_0",
        "does_not_cast_shadow",
        "search_cardinal_direction_lightmaps",
        ("not_a_pathfinding_obstacle", 1 << 3),
        "extension_of_parent",
        "does_not_cause_collision_damage",
        "early_mover",
        "early_mover_localized_physics",
        "use_static_massive_lightmap_sample",
        "object_scales_attachments",
        "inherits_player_s_appearance",
        "dead_bipeds_can_t_localize",
        "attach_to_clusters_by_dynamic_sphere",
        "effects_created_by_this_object_do_not_spawn_objects_in_multiplayer",
        ),
    Float("bounding_radius"),
    QStruct("bounding_offset", INCLUDE=xyz_float),
    Float("acceleration_scale"),
    SEnum16("lightmap_shadow_mode_size", *bloc_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *bloc_sweetener_size),
    SEnum8("water_density", *bloc_water_density),
    SInt32("unknown_0", VISIBLE=False),
    Float("dynamic_light_sphere_radius"),
    QStruct("dynamic_light_sphere_offset", INCLUDE=xyz_float),
    h3_string_id("default_model_variant"),
    h3_dependency("model"),
    h3_dependency("crate_object"),
    h3_dependency("collision_damage"),
    h3_reflexive("early_mover_properties", vehi_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", vehi_ai_propertie),
    h3_reflexive("functions", vehi_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", vehi_attachment),
    h3_reflexive("widgets", vehi_widget),
    h3_reflexive("change_colors", vehi_change_color),
    h3_reflexive("predicted_resources", vehi_predicted_resource),
    h3_reflexive("multiplayer_object_properties", vehi_multiplayer_object_propertie),
    Bool32("flags_1",
        "circular_aiming",
        "destroyed_after_dying",
        "half_speed_interpolation",
        "fires_from_camera",
        "entrance_inside_bounding_sphere",
        "doesn_t_show_readied_weapon",
        "causes_passenger_dialogue",
        "resists_pings",
        "melee_attack_is_fatal",
        "dont_reface_during_pings",
        "has_no_aiming",
        "simple_creature",
        "impact_melee_attaches_to_unit",
        "impact_melee_dies_on_shield",
        "cannot_open_doors_automatically",
        "melee_attackers_cannot_attach",
        "not_instantly_killed_by_melee",
        "shield_sapping",
        "runs_around_flaming",
        "inconsequential",
        "special_cinematic_unit",
        "ignored_by_autoaiming",
        "shields_fry_infection_forms",
        "can_dual_wield",
        ("acts_as_gunner_for_parent", 1 << 25),
        "controlled_by_parent_gunner",
        "parent_s_primary_weapon",
        "unit_has_boost",
        ),
    SEnum16("default_team", *crea_default_team),
    SEnum16("constant_sound_volume", *gint_constant_sound_volume),
    h3_reflexive("metagame_properties", vehi_metagame_propertie),
    h3_dependency("integrated_light_toggle"),
    float_rad("camera_field_of_view"),
    Float("camera_stiffness"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    h3_string_id("camera_marker_name"),
    h3_string_id("camera_submerged_marker_name"),
    float_rad("pitch_auto_level"),
    from_to_rad("pitch_range"),
    h3_reflexive("camera_tracks", vehi_camera_track),
    float_rad("unknown_4", VISIBLE=False),
    float_rad("unknown_5", VISIBLE=False),
    float_rad("unknown_6", VISIBLE=False),
    h3_reflexive("unknown_7", vehi_unknown_7),
    QStruct("acceleration_range", INCLUDE=ijk_float),
    Float("acceleration_action_scale"),
    Float("acceleration_attach_scale"),
    Float("soft_ping_threshold"),
    Float("soft_ping_interrupt_time"),
    Float("hard_ping_threshold"),
    Float("hard_ping_interrupt_time"),
    Float("feign_death_threshold"),
    Float("feign_death_time"),
    Float("distance_of_evade_animation"),
    Float("distance_of_dive_animation"),
    Float("stunned_movement_threshold"),
    Float("feign_death_chance"),
    Float("feign_repeat_chance"),
    h3_dependency("spawned_turret_character"),
    QStruct("spawned_actor_count", INCLUDE=from_to_sint16),
    Float("spawned_velocity"),
    float_rad("aiming_velocity_maximum"),
    float_rad("aiming_acceleration_maximum"),
    Float("casual_aiming_modifier"),
    float_rad("looking_velocity_maximum"),
    float_rad("looking_acceleration_maximum"),
    h3_string_id("right_hand_node"),
    h3_string_id("left_hand_node"),
    h3_string_id("preferred_gun_node"),
    h3_dependency("melee_damage"),
    h3_dependency("boarding_melee_damage"),
    h3_dependency("boarding_melee_response"),
    h3_dependency("ejection_melee_damage"),
    h3_dependency("ejection_melee_response"),
    h3_dependency("landing_melee_damage"),
    h3_dependency("flurry_melee_damage"),
    h3_dependency("obstacle_smash_damage"),
    SEnum16("motion_sensor_blip_size", *crea_motion_sensor_blip_size),
    SEnum16("item_scale", *gint_item_scale),
    h3_reflexive("postures", vehi_posture),
    h3_reflexive("hud_interfaces", vehi_hud_interface),
    h3_reflexive("dialogue_variants", vehi_dialogue_variant),
    Float("grenade_velocity"),
    SEnum16("grenade_type", *gint_grenade_type),
    SInt16("grenade_count"),
    h3_reflexive("powered_seats", vehi_powered_seat),
    h3_reflexive("weapons", vehi_weapon),
    h3_reflexive("seats", vehi_seat),
    Float("emp_radius"),
    h3_dependency("emp_effect"),
    h3_dependency("boost_collision_damage"),
    Float("boost_peak_power"),
    Float("boost_rise_power"),
    Float("boost_peak_time"),
    Float("boost_fall_power"),
    Float("boost_dead_time"),
    Float("lipsync_attack_weight"),
    Float("lipsync_decay_weight"),
    h3_dependency("detach_damage"),
    h3_dependency("detached_weapon"),
    Bool32("flags_2",
        "no_friction_with_driver",
        "can_trigger_automatic_opening_doors",
        "autoaim_when_teamless",
        "ai_weapon_cannot_rotate",
        "ai_does_not_require_driver",
        "ai_driver_enable",
        "ai_driver_flying",
        "ai_driver_can_sidestep",
        "ai_driver_hovering",
        "noncombat_vehicle",
        "vehicle_is_child",
        "bounces_at_death_barriers",
        "hydraulics",
        ),
    h3_reflexive("tank_engine_motion_properties", vehi_tank_engine_motion_propertie),
    h3_reflexive("engine_motion_properties", vehi_engine_motion_propertie),
    h3_reflexive("dropship_motion_properties", vehi_dropship_motion_propertie),
    h3_reflexive("antigravity_motion_properties", vehi_antigravity_motion_propertie),
    h3_reflexive("jet_engine_motion_properties", vehi_jet_engine_motion_propertie),
    h3_reflexive("turret_properties", vehi_turret_propertie),
    BytesRaw("unknown_8", SIZE=12, VISIBLE=False),
    h3_reflexive("helicopter_motion_properties", vehi_helicopter_motion_propertie),
    h3_reflexive("antigravity_engine_motion_properties", vehi_antigravity_engine_motion_propertie),
    h3_reflexive("autoturret_equipment", vehi_autoturret_equipment),
    Bool32("flags_3", *unknown_flags_32),
    Float("ground_friction"),
    Float("ground_depth"),
    Float("ground_damp_factor"),
    Float("ground_moving_friction"),
    Float("ground_maximum_slope_0"),
    Float("ground_maximum_slope_1_less_than_slope_0"),
    Float("unknown_9", VISIBLE=False),
    Float("anti_gravity_bank_lift"),
    Float("steering_bank_reaction_scale"),
    Float("gravity_scale"),
    Float("radius"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    h3_reflexive("anti_gravity_points", vehi_anti_gravity_point),
    h3_reflexive("friction_points", vehi_friction_point),
    h3_reflexive("phantom_shapes", vehi_phantom_shape),
    SEnum8("player_training_vehicle_type", *vehi_player_training_vehicle_type),
    SEnum8("vehicle_size", *vehi_vehicle_size),
    SInt8("unknown_13", VISIBLE=False),
    SInt8("unknown_14", VISIBLE=False),
    Float("minimum_flipping_angular_velocity"),
    Float("maximum_flipping_angular_velocity"),
    BytesRaw("unknown_15", SIZE=8, VISIBLE=False),
    Float("seat_entrance_acceleration_scale"),
    Float("seat_exit_acceleration_scale"),
    Float("flip_time"),
    h3_string_id("flip_over_message"),
    h3_dependency("suspension_sound"),
    h3_dependency("running_effect"),
    h3_dependency("unknown_response_0"),
    h3_dependency("unknown_response_1"),
    ENDIAN=">", SIZE=1100
    )


def get():
    return vehi_def

vehi_def = TagDef("vehi",
    h3_blam_header('vehi'),
    vehi_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["vehi"], endian=">", tag_cls=H3Tag
    )
