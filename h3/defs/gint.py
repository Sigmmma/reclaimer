from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

gint_ai_propertie_leap_jump_speed = (
    "none",
    "down",
    "step",
    "crouch",
    "stand",
    "storey",
    "tower",
    "infinite",
    )

gint_ai_propertie_size = (
    "default",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "immobile",
    )

gint_attachment_change_color = (
    "none",
    "primary",
    "secondary",
    "tertiary",
    "quaternary",
    )

gint_constant_sound_volume = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet",
    )

gint_default_team = (
    "default",
    "player",
    "human",
    "covenant",
    "flood",
    "sentinel",
    "heretic",
    "prophet",
    "guilty",
    "unused9",
    "unused10",
    "unused11",
    "unused12",
    "unused13",
    "unused14",
    "unused15",
    )

gint_grenade_type = (
    "human_fragmentation",
    "covenant_plasma",
    "brute_spike",
    "firebomb",
    )

gint_item_scale = (
    "small",
    "medium",
    "large",
    "huge",
    )

gint_lightmap_shadow_mode_size = (
    "default",
    "never",
    "always",
    "unknown",
    )

gint_metagame_propertie_classification = (
    "infantry",
    "leader",
    "hero",
    "specialist",
    "light_vehicle",
    "heavy_vehicle",
    "giant_vehicle",
    "standard_vehicle",
    )

gint_metagame_propertie_unit = (
    "brute",
    "grunt",
    "jackal",
    "marine",
    "bugger",
    "hunter",
    "flood_infection",
    "flood_carrier",
    "flood_combat",
    "flood_pureform",
    "sentinel",
    "elite",
    "turret",
    "mongoose",
    "warthog",
    "scorpion",
    "hornet",
    "pelican",
    "shade",
    "watchtower",
    "ghost",
    "chopper",
    "mauler",
    "wraith",
    "banshee",
    "phantom",
    "scarab",
    "guntower",
    )

gint_motion_sensor_blip_size = (
    "medium",
    "small",
    "large",
    )

gint_multiplayer_object_propertie_object_type = (
    "ordinary",
    "weapon",
    "grenade",
    "projectile",
    "powerup",
    "equipment",
    "light_land_vehicle",
    "heavy_land_vehicle",
    "flying_vehicle",
    "teleporter_2way",
    "teleporter_sender",
    "teleporter_receiver",
    "player_spawn_location",
    "player_respawn_zone",
    "hold_spawn_objective",
    "capture_spawn_objective",
    "hold_destination_objective",
    "capture_destination_objective",
    "hill_objective",
    "infection_haven_objective",
    "territory_objective",
    "vip_boundary_objective",
    "vip_destination_objective",
    "juggernaut_destination_objective",
    )

gint_multiplayer_object_propertie_shape = (
    "none",
    "sphere",
    "cylinder",
    "box",
    )

gint_multiplayer_object_propertie_spawn_timer_mode = (
    "on_death",
    "on_disturbance",
    )

gint_object_type = (
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
    )

gint_seat_ai_seat_type = (
    "none",
    "passenger",
    "gunner",
    "small_cargo",
    "large_cargo",
    "driver",
    )

gint_sweetener_size = (
    "small",
    "medium",
    "large",
    )

gint_water_density = (
    "default",
    "least",
    "some",
    "equal",
    "more",
    "more_still",
    "lots_more",
    )


gint_early_mover_propertie = Struct("early_mover_properties",
    string_id_meta("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


gint_ai_propertie = Struct("ai_properties",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    string_id_meta("ai_type_name"),
    Pad(4),
    SEnum16("size", *gint_ai_propertie_size),
    SEnum16("leap_jump_speed", *gint_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


gint_function = Struct("functions",
    Bool32("flags",
        "invert",
        "mapping_does_not_controls_active",
        "always_active",
        "random_time_offset",
        ),
    string_id_meta("import_name"),
    string_id_meta("export_name"),
    string_id_meta("turn_off_with"),
    Float("minimum_value"),
    rawdata_ref("default_function"),
    string_id_meta("scale_by"),
    ENDIAN=">", SIZE=44
    )


gint_attachment = Struct("attachments",
    dependency("attachment"),
    string_id_meta("marker"),
    SEnum16("change_color", *gint_attachment_change_color),
    SInt16("unknown"),
    string_id_meta("primary_scale"),
    string_id_meta("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


gint_widget = Struct("widgets",
    dependency("type"),
    ENDIAN=">", SIZE=16
    )


gint_change_color_initial_permutation = Struct("initial_permutations",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    string_id_meta("variant_name"),
    ENDIAN=">", SIZE=32
    )


gint_change_color_function = Struct("functions",
    Bool32("scale_flags",
        "blend_in_hsv",
        "more_colors",
        ),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    string_id_meta("darken_by"),
    string_id_meta("scale_by"),
    ENDIAN=">", SIZE=32
    )


gint_change_color = Struct("change_colors",
    reflexive("initial_permutations", gint_change_color_initial_permutation),
    reflexive("functions", gint_change_color_function),
    ENDIAN=">", SIZE=24
    )


gint_predicted_resource = Struct("predicted_resources",
    SInt16("type"),
    SInt16("resource_index"),
    UInt32("tag_index"),
    ENDIAN=">", SIZE=8
    )


gint_multiplayer_object_propertie = Struct("multiplayer_object_properties",
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
    SEnum8("object_type", *gint_multiplayer_object_propertie_object_type),
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
    SEnum8("shape", *gint_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *gint_multiplayer_object_propertie_spawn_timer_mode),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    Float("radius_width"),
    Float("length"),
    Float("top"),
    Float("bottom"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    SInt32("unknown_3"),
    SInt32("unknown_4"),
    dependency("child_object"),
    SInt32("unknown_5"),
    dependency("shape_shader"),
    dependency("unknown_shader"),
    dependency("unknown_6"),
    dependency("unknown_7"),
    dependency("unknown_8"),
    dependency("unknown_9"),
    dependency("unknown_10"),
    dependency("unknown_11"),
    ENDIAN=">", SIZE=196
    )


gint_metagame_propertie = Struct("metagame_properties",
    Bool8("flags",
        "must_have_active_seats",
        ),
    SEnum8("unit", *gint_metagame_propertie_unit),
    SEnum8("classification", *gint_metagame_propertie_classification),
    SInt8("unknown"),
    SInt16("points"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=8
    )


gint_camera_track = Struct("camera_tracks",
    dependency("track"),
    ENDIAN=">", SIZE=16
    )


gint_unknown_7 = Struct("unknown_7",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("unknown_14"),
    Float("unknown_15"),
    Float("unknown_16"),
    Float("unknown_17"),
    Float("unknown_18"),
    ENDIAN=">", SIZE=76
    )


gint_posture = Struct("postures",
    string_id_meta("name"),
    Float("pill_offset_i"),
    Float("pill_offset_j"),
    Float("pill_offset_k"),
    ENDIAN=">", SIZE=16
    )


gint_hud_interface = Struct("hud_interfaces",
    dependency("unit_hud_interface"),
    ENDIAN=">", SIZE=16
    )


gint_dialogue_variant = Struct("dialogue_variants",
    SInt16("variant_number"),
    SInt16("unknown"),
    dependency("dialogue"),
    ENDIAN=">", SIZE=20
    )


gint_powered_seat = Struct("powered_seats",
    Float("driver_powerup_time"),
    Float("driver_powerdown_time"),
    ENDIAN=">", SIZE=8
    )


gint_weapon = Struct("weapons",
    dependency("weapon"),
    ENDIAN=">", SIZE=16
    )


gint_seat_camera_track = Struct("camera_tracks",
    dependency("track"),
    ENDIAN=">", SIZE=16
    )


gint_seat_unknown_6 = Struct("unknown_6",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("unknown_14"),
    Float("unknown_15"),
    Float("unknown_16"),
    Float("unknown_17"),
    Float("unknown_18"),
    ENDIAN=">", SIZE=76
    )


gint_seat_unit_hud_interface = Struct("unit_hud_interface",
    dependency("unit_hud_interface"),
    ENDIAN=">", SIZE=16
    )


gint_seat = Struct("seats",
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
    string_id_meta("seat_animation"),
    string_id_meta("seat_marker_name"),
    string_id_meta("entry_marker_s_name"),
    string_id_meta("boarding_grenade_marker"),
    string_id_meta("boarding_grenade_string"),
    string_id_meta("boarding_melee_string"),
    string_id_meta("detach_weapon_string"),
    Float("ping_scale"),
    Float("turnover_time"),
    Float("acceleration_range_i"),
    Float("acceleration_range_j"),
    Float("acceleration_range_k"),
    Float("acceleration_action_scale"),
    Float("acceleration_attach_scale"),
    Float("ai_scariness"),
    SEnum16("ai_seat_type", *gint_seat_ai_seat_type),
    SInt16("boarding_seat"),
    Float("listener_interpolation_factor"),
    Float("yaw_rate_bounds_min"),
    Float("yaw_rate_bounds_max"),
    Float("pitch_rate_bounds_min"),
    Float("pitch_rate_bounds_max"),
    Float("unknown"),
    Float("minimum_speed_reference"),
    Float("maximum_speed_reference"),
    Float("speed_exponent"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    string_id_meta("camera_marker_name"),
    string_id_meta("camera_submerged_marker_name"),
    float_rad("pitch_auto_level"),
    float_rad("pitch_range_min"),
    float_rad("pitch_range_max"),
    reflexive("camera_tracks", gint_seat_camera_track),
    float_rad("unknown_3"),
    float_rad("unknown_4"),
    float_rad("unknown_5"),
    reflexive("unknown_6", gint_seat_unknown_6),
    reflexive("unit_hud_interface", gint_seat_unit_hud_interface),
    string_id_meta("enter_seat_string"),
    float_rad("yaw_range_min"),
    float_rad("yaw_range_max"),
    dependency("built_in_gunner"),
    Float("entry_radius"),
    float_rad("entry_marker_cone_angle"),
    float_rad("entry_marker_facing_angle"),
    Float("maximum_relative_velocity"),
    string_id_meta("invisible_seat_region"),
    SInt32("runtime_invisible_seat_region_index"),
    ENDIAN=">", SIZE=228
    )


gint_buckling_parameter = Struct("buckling_parameters",
    Float("unknown"),
    SInt32("unknown_1"),
    Float("unknown_2"),
    SInt32("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    string_id_meta("marker"),
    Float("scan_distance_1_float"),
    Float("scan_distance_2_float"),
    SInt32("scan_distance_1_integer"),
    SInt32("scan_distance_2_integer"),
    float_rad("min"),
    float_rad("max"),
    float_rad("min_1"),
    float_rad("max_1"),
    string_id_meta("buckle_animation"),
    string_id_meta("buckle_wobble_animation"),
    string_id_meta("buckle_wobble_animation_1"),
    Float("unknown_9"),
    Float("unknown_10"),
    ENDIAN=">", SIZE=92
    )


gint_meta_def = BlockDef("gint",
    SEnum16("object_type", *gint_object_type),
    Bool16("flags",
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
    Float("bounding_offset_x"),
    Float("bounding_offset_y"),
    Float("bounding_offset_z"),
    Float("acceleration_scale"),
    SEnum16("lightmap_shadow_mode_size", *gint_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *gint_sweetener_size),
    SEnum8("water_density", *gint_water_density),
    SInt32("unknown"),
    Float("dynamic_light_sphere_radius"),
    Float("dynamic_light_sphere_offset_x"),
    Float("dynamic_light_sphere_offset_y"),
    Float("dynamic_light_sphere_offset_z"),
    string_id_meta("default_model_variant"),
    dependency("model"),
    dependency("crate_object"),
    dependency("collision_damage"),
    reflexive("early_mover_properties", gint_early_mover_propertie),
    dependency("creation_effect"),
    dependency("material_effects"),
    dependency("melee_impact"),
    reflexive("ai_properties", gint_ai_propertie),
    reflexive("functions", gint_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1"),
    reflexive("attachments", gint_attachment),
    reflexive("widgets", gint_widget),
    reflexive("change_colors", gint_change_color),
    reflexive("predicted_resources", gint_predicted_resource),
    reflexive("multiplayer_object_properties", gint_multiplayer_object_propertie),
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
        "don_t_reface_during_pings",
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
    SEnum16("default_team", *gint_default_team),
    SEnum16("constant_sound_volume", *gint_constant_sound_volume),
    reflexive("metagame_properties", gint_metagame_propertie),
    dependency("integrated_light_toggle"),
    float_rad("camera_field_of_view"),
    Float("camera_stiffness"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    string_id_meta("camera_marker_name"),
    string_id_meta("camera_submerged_marker_name"),
    float_rad("pitch_auto_level"),
    float_rad("pitch_range_min"),
    float_rad("pitch_range_max"),
    reflexive("camera_tracks", gint_camera_track),
    float_rad("unknown_4"),
    float_rad("unknown_5"),
    float_rad("unknown_6"),
    reflexive("unknown_7", gint_unknown_7),
    Float("acceleration_range_i"),
    Float("acceleration_range_j"),
    Float("acceleration_range_k"),
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
    dependency("spawned_turret_character"),
    SInt16("spawned_actor_count_min"),
    SInt16("spawned_actor_count_max"),
    Float("spawned_velocity"),
    float_rad("aiming_velocity_maximum"),
    float_rad("aiming_acceleration_maximum"),
    Float("casual_aiming_modifier"),
    float_rad("looking_velocity_maximum"),
    float_rad("looking_acceleration_maximum"),
    string_id_meta("right_hand_node"),
    string_id_meta("left_hand_node"),
    string_id_meta("preferred_gun_node"),
    dependency("melee_damage"),
    dependency("boarding_melee_damage"),
    dependency("boarding_melee_response"),
    dependency("ejection_melee_damage"),
    dependency("ejection_melee_response"),
    dependency("landing_melee_damage"),
    dependency("flurry_melee_damage"),
    dependency("obstacle_smash_damage"),
    SEnum16("motion_sensor_blip_size", *gint_motion_sensor_blip_size),
    SEnum16("item_scale", *gint_item_scale),
    reflexive("postures", gint_posture),
    reflexive("hud_interfaces", gint_hud_interface),
    reflexive("dialogue_variants", gint_dialogue_variant),
    Float("grenade_velocity"),
    SEnum16("grenade_type", *gint_grenade_type),
    SInt16("grenade_count"),
    reflexive("powered_seats", gint_powered_seat),
    reflexive("weapons", gint_weapon),
    reflexive("seats", gint_seat),
    Float("emp_radius"),
    dependency("emp_effect"),
    dependency("boost_collision_damage"),
    Float("boost_peak_power"),
    Float("boost_rise_power"),
    Float("boost_peak_time"),
    Float("boost_fall_power"),
    Float("boost_dead_time"),
    Float("lipsync_attack_weight"),
    Float("lipsync_decay_weight"),
    dependency("detach_damage"),
    dependency("detached_weapon"),
    Pad(4),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("animation_speed"),
    Float("vertical_force"),
    Float("leg_attach_radius"),
    reflexive("buckling_parameters", gint_buckling_parameter),
    Float("toe_joint_extended_fraction"),
    TYPE=Struct, ENDIAN=">", SIZE=820
    )