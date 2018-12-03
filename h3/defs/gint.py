############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	put in flags, bounding info, named tags, attachments, seats, cameras
# revision: 3		author: Lord Zedd
# 	Portin'
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


gint_early_mover_propertie = Struct("early_mover_propertie", 
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


gint_ai_propertie = Struct("ai_propertie", 
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


gint_function = Struct("function", 
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


gint_attachment = Struct("attachment", 
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


gint_widget = Struct("widget", 
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


gint_change_color_initial_permutation = Struct("initial_permutation", 
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


gint_change_color_function = Struct("function", 
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


gint_change_color = Struct("change_color", 
    h3_reflexive("initial_permutations", gint_change_color_initial_permutation),
    h3_reflexive("functions", gint_change_color_function),
    ENDIAN=">", SIZE=24
    )


gint_predicted_resource = Struct("predicted_resource", 
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


gint_multiplayer_object_propertie = Struct("multiplayer_object_propertie", 
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


gint_metagame_propertie = Struct("metagame_propertie", 
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


gint_camera_track = Struct("camera_track", 
    h3_dependency("track"),
    ENDIAN=">", SIZE=16
    )


gint_unknown_7 = Struct("unknown_7", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=19, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=76
    )


gint_posture = Struct("posture", 
    h3_string_id("name"),
    QStruct("pill_offset", INCLUDE=ijk_float),
    ENDIAN=">", SIZE=16
    )


gint_hud_interface = Struct("hud_interface", 
    h3_dependency("unit_hud_interface"),
    ENDIAN=">", SIZE=16
    )


gint_dialogue_variant = Struct("dialogue_variant", 
    SInt16("variant_number"),
    SInt16("unknown", VISIBLE=False),
    h3_dependency("dialogue"),
    ENDIAN=">", SIZE=20
    )


gint_powered_seat = Struct("powered_seat", 
    Float("driver_powerup_time"),
    Float("driver_powerdown_time"),
    ENDIAN=">", SIZE=8
    )


gint_weapon = Struct("weapon", 
    h3_dependency("weapon"),
    ENDIAN=">", SIZE=16
    )


gint_seat_camera_track = Struct("camera_track", 
    h3_dependency("track"),
    ENDIAN=">", SIZE=16
    )


gint_seat_unknown_6 = Struct("unknown_6", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=19, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=76
    )


gint_seat_unit_hud_interface = Struct("unit_hud_interface", 
    h3_dependency("unit_hud_interface"),
    ENDIAN=">", SIZE=16
    )


gint_seat = Struct("seat", 
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
    h3_reflexive("camera_tracks", gint_seat_camera_track),
    float_rad("unknown_3", VISIBLE=False),
    float_rad("unknown_4", VISIBLE=False),
    float_rad("unknown_5", VISIBLE=False),
    h3_reflexive("unknown_6", gint_seat_unknown_6),
    h3_reflexive("unit_hud_interface", gint_seat_unit_hud_interface),
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


gint_buckling_parameter = Struct("buckling_parameter", 
    Float("unknown_0"),
    SInt32("unknown_1"),
    Float("unknown_2"),
    SInt32("unknown_3"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=5),
    h3_string_id("marker"),
    Float("scan_distance_1_float"),
    Float("scan_distance_2_float"),
    SInt32("scan_distance_1_integer"),
    SInt32("scan_distance_2_integer"),
    float_rad("min_0"),
    float_rad("max_0"),
    float_rad("min_1"),
    float_rad("max_1"),
    h3_string_id("buckle_animation"),
    h3_string_id("buckle_wobble_animation_0"),
    h3_string_id("buckle_wobble_animation_1"),
    Float("unknown_4"),
    Float("unknown_5"),
    ENDIAN=">", SIZE=92
    )


gint_body = Struct("tagdata", 
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
    h3_reflexive("early_mover_properties", gint_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", gint_ai_propertie),
    h3_reflexive("functions", gint_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", gint_attachment),
    h3_reflexive("widgets", gint_widget),
    h3_reflexive("change_colors", gint_change_color),
    h3_reflexive("predicted_resources", gint_predicted_resource),
    h3_reflexive("multiplayer_object_properties", gint_multiplayer_object_propertie),
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
    h3_reflexive("metagame_properties", gint_metagame_propertie),
    h3_dependency("integrated_light_toggle"),
    float_rad("camera_field_of_view"),
    Float("camera_stiffness"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    h3_string_id("camera_marker_name"),
    h3_string_id("camera_submerged_marker_name"),
    float_rad("pitch_auto_level"),
    from_to_rad("pitch_range"),
    h3_reflexive("camera_tracks", gint_camera_track),
    float_rad("unknown_4", VISIBLE=False),
    float_rad("unknown_5", VISIBLE=False),
    float_rad("unknown_6", VISIBLE=False),
    h3_reflexive("unknown_7", gint_unknown_7),
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
    h3_reflexive("postures", gint_posture),
    h3_reflexive("hud_interfaces", gint_hud_interface),
    h3_reflexive("dialogue_variants", gint_dialogue_variant),
    Float("grenade_velocity"),
    SEnum16("grenade_type", *gint_grenade_type),
    SInt16("grenade_count"),
    h3_reflexive("powered_seats", gint_powered_seat),
    h3_reflexive("weapons", gint_weapon),
    h3_reflexive("seats", gint_seat),
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
    Pad(4),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("animation_speed"),
    Float("vertical_force"),
    Float("leg_attach_radius"),
    h3_reflexive("buckling_parameters", gint_buckling_parameter),
    Float("toe_joint_extended_fraction"),
    ENDIAN=">", SIZE=820
    )


def get():
    return gint_def

gint_def = TagDef("gint",
    h3_blam_header('gint'),
    gint_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["gint"], endian=">", tag_cls=H3Tag
    )