from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

weap_ai_propertie_leap_jump_speed = (
    "none",
    "down",
    "step",
    "crouch",
    "stand",
    "storey",
    "tower",
    "infinite",
    )

weap_ai_propertie_size = (
    "default",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "immobile",
    )

weap_attachment_change_color = (
    "none",
    "primary",
    "secondary",
    "tertiary",
    "quaternary",
    )

weap_barrel_angle_change_function = (
    "linear",
    "early",
    "very_early",
    "late",
    "very_late",
    "cosine",
    "one",
    "zero",
    )

weap_barrel_distribution_function = (
    "point",
    "horizontal_fan",
    )

weap_barrel_firing_noise = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet",
    )

weap_barrel_prediction_type = (
    "none",
    "continuous",
    "instant",
    )

weap_lightmap_shadow_mode_size = (
    "default",
    "never",
    "always",
    "unknown",
    )

weap_melee_damage_reporting_type = (
    "guardians",
    "falling_damage",
    "collision",
    "melee",
    "explosion",
    "magnum",
    "plasma_pistol",
    "needler",
    "mauler",
    "smg",
    "plasma_rifle",
    "battle_rifle",
    "carbine",
    "shotgun",
    "sniper_rifle",
    "beam_rifle",
    "assault_rifle",
    "spiker",
    "fuel_rod_cannon",
    "missile_pod",
    "rocket_launcher",
    "spartan_laser",
    "brute_shot",
    "flamethrower",
    "sentinel_gun",
    "energy_sword",
    "gravity_hammer",
    "frag_grenade",
    "plasma_grenade",
    "spike_grenade",
    "firebomb_grenade",
    "flag",
    "bomb",
    "bomb_explosion",
    "ball",
    "machinegun_turret",
    "plasma_cannon",
    "plasma_mortar",
    "plasma_turret",
    "banshee",
    "ghost",
    "mongoose",
    "scorpion",
    "scorpion_gunner",
    "spectre",
    "spectre_gunner",
    "warthog",
    "warthog_gunner",
    "warthog_gauss_turret",
    "wraith",
    "wraith_gunner",
    "tank",
    "chopper",
    "hornet",
    "mantis",
    "prowler",
    "sentinel_beam",
    "sentinel_rpg",
    "teleporter",
    "tripmine",
    "elephant_turret",
    )

weap_movement_penalized = (
    "always",
    "when_zoomed",
    "when_zoomed_or_reloading",
    )

weap_multiplayer_object_propertie_object_type = (
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

weap_multiplayer_object_propertie_shape = (
    "none",
    "sphere",
    "cylinder",
    "box",
    )

weap_multiplayer_object_propertie_spawn_timer_mode = (
    "on_death",
    "on_disturbance",
    )

weap_multiplayer_weapon_type = (
    "none",
    "ctf_flag",
    "oddball_ball",
    "headhunter_head",
    "juggernaut_powerup",
    )

weap_new_trigger_behavior = (
    "spew",
    "latch",
    "latch_autofire",
    "charge",
    "latch_zoom",
    "latch_rocketlauncher",
    "spew_charge",
    )

weap_new_trigger_button_used = (
    "right_trigger",
    "left_trigger",
    "melee_attack",
    "automated_fire",
    "right_bumper",
    )

weap_new_trigger_overcharge_action = (
    "none",
    "explode",
    "discharge",
    )

weap_new_trigger_prediction = (
    "none",
    "spew",
    "charge",
    )

weap_new_trigger_secondary_action = (
    "fire",
    "charge",
    "track",
    "fire_other",
    )

weap_object_type = (
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

weap_secondary_trigger_mode = (
    "normal",
    "slaved_to_primary",
    "inhibits_primary",
    "loads_alternate_ammunition",
    "loads_multiple_primary_ammunition",
    )

weap_sweetener_size = (
    "small",
    "medium",
    "large",
    )

weap_tracking_type = (
    "no_tracking",
    "human_tracking",
    "plasma_tracking",
    )

weap_water_density = (
    "default",
    "least",
    "some",
    "equal",
    "more",
    "more_still",
    "lots_more",
    )

weap_weapon_type = (
    "undefined",
    "shotgun",
    "needler",
    "plasma_pistol",
    "plasma_rifle",
    "rocket_launcher",
    "energy_sword",
    "spartan_laser",
    )


weap_early_mover_propertie = Struct("early_mover_properties",
    string_id_meta("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


weap_ai_propertie = Struct("ai_properties",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    string_id_meta("ai_type_name"),
    Pad(4),
    SEnum16("size", *weap_ai_propertie_size),
    SEnum16("leap_jump_speed", *weap_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


weap_function = Struct("functions",
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


weap_attachment = Struct("attachments",
    dependency("attachment"),
    string_id_meta("marker"),
    SEnum16("change_color", *weap_attachment_change_color),
    SInt16("unknown"),
    string_id_meta("primary_scale"),
    string_id_meta("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


weap_widget = Struct("widgets",
    dependency("type"),
    ENDIAN=">", SIZE=16
    )


weap_change_color_initial_permutation = Struct("initial_permutations",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    string_id_meta("variant_name"),
    ENDIAN=">", SIZE=32
    )


weap_change_color_function = Struct("functions",
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


weap_change_color = Struct("change_colors",
    reflexive("initial_permutations", weap_change_color_initial_permutation),
    reflexive("functions", weap_change_color_function),
    ENDIAN=">", SIZE=24
    )


weap_predicted_resource = Struct("predicted_resources",
    SInt16("type"),
    SInt16("resource_index"),
    UInt32("tag_index"),
    ENDIAN=">", SIZE=8
    )


weap_multiplayer_object_propertie = Struct("multiplayer_object_properties",
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
    SEnum8("object_type", *weap_multiplayer_object_propertie_object_type),
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
    SEnum8("shape", *weap_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *weap_multiplayer_object_propertie_spawn_timer_mode),
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


weap_predicted_bitmap = Struct("predicted_bitmaps",
    dependency("bitmap"),
    ENDIAN=">", SIZE=16
    )


weap_first_person = Struct("first_person",
    dependency("first_person_model"),
    dependency("first_person_animations"),
    ENDIAN=">", SIZE=32
    )


weap_predicted_resources_1 = Struct("predicted_resources_1",
    SInt16("type"),
    SInt16("resource_index"),
    UInt32("tag_index"),
    ENDIAN=">", SIZE=8
    )


weap_magazine_magazine_equipment = Struct("magazine_equipment",
    SInt16("rounds_0_for_max"),
    SInt16("unknown"),
    dependency("equipment"),
    ENDIAN=">", SIZE=20
    )


weap_magazine = Struct("magazines",
    Bool32("flags",
        "wastes_rounds_when_reloaded",
        "every_round_must_be_chambered",
        ),
    SInt16("rounds_recharged"),
    SInt16("rounds_total_initial"),
    SInt16("rounds_total_maximum"),
    SInt16("rounds_total_loaded_maximum"),
    SInt16("maximum_rounds_held"),
    SInt16("unknown"),
    Float("reload_time"),
    SInt16("rounds_reloaded"),
    SInt16("unknown_1"),
    Float("chamber_time"),
    Pad(24),
    dependency("reloading_effect"),
    dependency("reloading_damage_effect"),
    dependency("chambering_effect"),
    dependency("chambering_damage_effect"),
    reflexive("magazine_equipment", weap_magazine_magazine_equipment),
    ENDIAN=">", SIZE=128
    )


weap_new_trigger = Struct("new_triggers",
    Bool32("flags",
        "autofire_single_action_only",
        ),
    SEnum16("button_used", *weap_new_trigger_button_used),
    SEnum16("behavior", *weap_new_trigger_behavior),
    SInt16("primary_barrel"),
    SInt16("secondary_barrel"),
    SEnum16("prediction", *weap_new_trigger_prediction),
    SInt16("unknown"),
    Float("autofire_time"),
    Float("autofire_throw"),
    SEnum16("secondary_action", *weap_new_trigger_secondary_action),
    SEnum16("primary_action", *weap_new_trigger_secondary_action),
    Float("charging_time"),
    Float("charged_time"),
    SEnum16("overcharge_action", *weap_new_trigger_overcharge_action),
    Bool16("charge_flags",
        ),
    Float("charged_illumination"),
    Float("spew_time"),
    dependency("charging_effect"),
    dependency("charging_damage_effect"),
    dependency("charging_response"),
    Float("charging_age_degeneration"),
    dependency("discharging_effect"),
    dependency("discharging_damage_effect"),
    Float("target_tracking_decay_time"),
    Pad(4),
    Float("unknown_2"),
    ENDIAN=">", SIZE=144
    )


weap_barrel_first_person_offset = Struct("first_person_offsets",
    Float("first_person_offset_x"),
    Float("first_person_offset_y"),
    Float("first_person_offset_z"),
    ENDIAN=">", SIZE=12
    )


weap_barrel_firing_effect = Struct("firing_effects",
    SInt16("shot_count_lower_bound"),
    SInt16("shot_count_upper_bound"),
    dependency("firing_effect"),
    dependency("misfire_effect"),
    dependency("empty_effect"),
    dependency("unknown_effect"),
    dependency("firing_response"),
    dependency("misfire_response"),
    dependency("empty_response"),
    dependency("unknown_response"),
    dependency("rider_firing_response"),
    dependency("rider_misfire_response"),
    dependency("rider_empty_response"),
    dependency("rider_unknown_response"),
    ENDIAN=">", SIZE=196
    )


weap_barrel = Struct("barrels",
    Bool32("flags",
        "tracks_fired_projectile",
        "random_firing_effects",
        "can_fire_with_partial_ammo",
        "projectiles_use_weapon_origin",
        "ejects_during_chamber",
        "use_error_when_unzoomed",
        "projectile_vector_cannot_be_adjusted",
        "projectiles_have_identical_error",
        "projectiles_fire_parallel",
        "cant_fire_when_others_firing",
        "cant_fire_when_others_recovering",
        "don_t_clear_fire_bit_after_recovering",
        "stagger_fire_across_multiple_markers",
        "fires_locked_projectiles",
        ),
    Float("rounds_per_second_min"),
    Float("rounds_per_second_max"),
    Float("acceleration_time"),
    Float("deceleration_time"),
    Float("barrel_spin_scale"),
    Float("blurred_rate_of_fire"),
    SInt16("shots_per_fire_min"),
    SInt16("shots_per_fire_max"),
    Float("fire_recovery_time"),
    Float("soft_recovery_fraction"),
    SInt16("magazine"),
    SInt16("rounds_per_shot"),
    SInt16("minimum_rounds_loaded"),
    SInt16("rounds_between_tracers"),
    string_id_meta("optional_barrel_marker_name"),
    SEnum16("prediction_type", *weap_barrel_prediction_type),
    SEnum16("firing_noise", *weap_barrel_firing_noise),
    Float("acceleration_time_1"),
    Float("deceleration_time_1"),
    Float("damage_error_min"),
    Float("damage_error_max"),
    float_rad("base_turning_speed"),
    float_rad("dynamic_turning_speed_min"),
    float_rad("dynamic_turning_speed_max"),
    Float("acceleration_time_2"),
    Float("deceleration_time_2"),
    Float("unknown"),
    Float("unknown_1"),
    float_rad("minimum_error"),
    float_rad("error_angle_min"),
    float_rad("error_angle_max"),
    Float("dual_wield_damage_scale"),
    SEnum16("distribution_function", *weap_barrel_distribution_function),
    SInt16("projectiles_per_shot"),
    float_rad("distribution_angle"),
    float_rad("minimum_error_1"),
    float_rad("error_angle_min_1"),
    float_rad("error_angle_max_1"),
    reflexive("first_person_offsets", weap_barrel_first_person_offset),
    SEnum8("damage_reporting_type", *weap_melee_damage_reporting_type),
    SInt8("unknown_2"),
    SInt16("unknown_3"),
    dependency("initial_projectile"),
    dependency("trailing_projectile"),
    dependency("damage_effect"),
    dependency("crate_projectile"),
    Float("crate_projectile_speed"),
    Float("ejection_port_recovery_time"),
    Float("illumination_recovery_time"),
    Float("heat_generated_per_round"),
    Float("age_generated_per_round_mp"),
    Float("age_generated_per_round_sp"),
    Float("overload_time"),
    float_rad("angle_change_per_shot_min"),
    float_rad("angle_change_per_shot_max"),
    Pad(8),
    SEnum16("angle_change_function", *weap_barrel_angle_change_function),
    SInt16("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("firing_effect_deceleration_time"),
    Float("unknown_7"),
    Float("rate_of_fire_acceleration_time"),
    Float("rate_of_fire_deceleration_time"),
    Float("unknown_8"),
    Float("unknown_9"),
    reflexive("firing_effects", weap_barrel_firing_effect),
    ENDIAN=">", SIZE=308
    )


weap_meta_def = BlockDef("weap",
    SEnum16("object_type", *weap_object_type),
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
    SEnum16("lightmap_shadow_mode_size", *weap_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *weap_sweetener_size),
    SEnum8("water_density", *weap_water_density),
    SInt32("unknown"),
    Float("dynamic_light_sphere_radius"),
    Float("dynamic_light_sphere_offset_x"),
    Float("dynamic_light_sphere_offset_y"),
    Float("dynamic_light_sphere_offset_z"),
    string_id_meta("default_model_variant"),
    dependency("model"),
    dependency("crate_object"),
    dependency("collision_damage"),
    reflexive("early_mover_properties", weap_early_mover_propertie),
    dependency("creation_effect"),
    dependency("material_effects"),
    dependency("melee_impact"),
    reflexive("ai_properties", weap_ai_propertie),
    reflexive("functions", weap_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1"),
    reflexive("attachments", weap_attachment),
    reflexive("widgets", weap_widget),
    reflexive("change_colors", weap_change_color),
    reflexive("predicted_resources", weap_predicted_resource),
    reflexive("multiplayer_object_properties", weap_multiplayer_object_propertie),
    Bool32("flags_1",
        "always_maintains_z_up",
        "destroyed_by_explosions",
        "unaffected_by_gravity",
        ),
    SInt16("old_message_index"),
    SInt16("sort_order"),
    Float("old_multiplayer_on_ground_scale"),
    Float("old_campaign_on_ground_scale"),
    string_id_meta("pickup_message"),
    string_id_meta("swap_message"),
    string_id_meta("pickup_or_dual_wield_message"),
    string_id_meta("swap_or_dual_wield_message"),
    string_id_meta("picked_up_message"),
    string_id_meta("switch_to_message"),
    string_id_meta("switch_to_from_ai_message"),
    string_id_meta("all_weapons_empty_message"),
    dependency("collision_sound"),
    reflexive("predicted_bitmaps", weap_predicted_bitmap),
    dependency("detonation_damage_effect"),
    Float("detonation_delay_min"),
    Float("detonation_delay_max"),
    dependency("detonating_effect"),
    dependency("detonation_effect"),
    Float("campaign_ground_scale"),
    Float("multiplayer_ground_scale"),
    Float("small_hold_scale"),
    Float("small_holster_scale"),
    Float("medium_hold_scale"),
    Float("medium_holster_scale"),
    Float("large_hold_scale"),
    Float("large_holster_scale"),
    Float("huge_hold_scale"),
    Float("huge_holster_scale"),
    Float("grounded_friction_length"),
    Float("grounded_friction_unknown"),
    Bool32("flags_2",
        "vertical_heat_display",
        "mutually_exclusive_triggers",
        "attacks_automatically_on_bump",
        "must_be_readied",
        "doesn_t_count_towards_maximum",
        "aim_assists_only_when_zoomed",
        "prevents_grenade_throwing",
        "must_be_picked_up",
        "holds_triggers_when_dropped",
        "prevents_melee_attack",
        "detonates_when_dropped",
        "cannot_fire_at_maximum_age",
        "secondary_trigger_overrides_grenades",
        "does_not_depower_active_camo_in_multiplayer",
        "enables_integrated_night_vision",
        "ais_use_weapon_melee_damage",
        "forces_no_binoculars",
        "loop_fp_firing_animation",
        "prevents_sprinting",
        "cannot_fire_while_boosting",
        "prevents_driving",
        "third_person_camera",
        "can_be_dual_wielded",
        "can_only_be_dual_wielded",
        "melee_only",
        "can_t_fire_if_parent_dead",
        "weapon_ages_with_each_kill",
        "weapon_uses_old_dual_fire_error_code",
        "primary_trigger_melee_attacks",
        "cannot_be_used_by_player",
        ),
    Bool32("more_flags",
        ),
    string_id_meta("unknown_2"),
    SEnum16("secondary_trigger_mode", *weap_secondary_trigger_mode),
    SInt16("maximum_alternate_shots_loaded"),
    Float("turn_on_time"),
    Float("ready_time"),
    dependency("ready_effect"),
    dependency("ready_damage_effect"),
    Float("heat_recovery_threshold"),
    Float("overheated_threshold"),
    Float("heat_detonation_threshold"),
    Float("heat_detonation_fraction"),
    Float("heat_loss_per_second"),
    Float("heat_illumination"),
    Float("overheated_heat_loss_per_second"),
    dependency("overheated"),
    dependency("overheated_damage_effect"),
    dependency("detonation"),
    dependency("detonation_damage_effect_1"),
    dependency("player_melee_damage"),
    dependency("player_melee_response"),
    float_rad("damage_pyramid_angles_y"),
    float_rad("damage_pyramid_angles_p"),
    Float("damage_pyramid_depth"),
    dependency("_1st_hit_damage"),
    dependency("_1st_hit_response"),
    dependency("_2nd_hit_damage"),
    dependency("_2nd_hit_response"),
    dependency("_3rd_hit_damage"),
    dependency("_3rd_hit_response"),
    dependency("lunge_melee_damage"),
    dependency("lunge_melee_response"),
    dependency("gun_gun_clang_damage"),
    dependency("gun_gun_clang_response"),
    dependency("gun_sword_clang_damage"),
    dependency("gun_sword_clang_response"),
    dependency("clash_effect"),
    SEnum8("melee_damage_reporting_type", *weap_melee_damage_reporting_type),
    SInt8("unknown_3"),
    SInt16("magnification_levels"),
    Float("magnification_range_min"),
    Float("magnification_range_max"),
    float_rad("autoaim_angle"),
    Float("autoaim_range_long"),
    Float("autoaim_range_short"),
    float_rad("magnetism_angle"),
    Float("magnetism_range_long"),
    Float("magnetism_range_short"),
    float_rad("deviation_angle"),
    Pad(20),
    SEnum16("movement_penalized", *weap_movement_penalized),
    SInt16("unknown_5"),
    Float("forwards_movement_penalty"),
    Float("sideways_movement_penalty"),
    Float("ai_scariness"),
    Float("weapon_power_on_time"),
    Float("weapon_power_off_time"),
    dependency("weapon_power_on_effect"),
    dependency("weapon_power_off_effect"),
    Float("age_heat_recovery_penalty"),
    Float("age_rate_of_fire_penalty"),
    Float("age_misfire_start"),
    Float("age_misfire_chance"),
    dependency("pickup_sound"),
    dependency("zoom_in_sound"),
    dependency("zoom_out_sound"),
    Float("active_camo_ding"),
    Float("active_camo_regrowth_rate"),
    string_id_meta("handle_node"),
    string_id_meta("weapon_class"),
    string_id_meta("weapon_name"),
    SEnum16("multiplayer_weapon_type", *weap_multiplayer_weapon_type),
    SEnum16("weapon_type", *weap_weapon_type),
    SEnum16("tracking_type", *weap_tracking_type),
    SInt16("unknown_6"),
    Pad(16),
    reflexive("first_person", weap_first_person),
    dependency("hud_interface"),
    reflexive("predicted_resources_1", weap_predicted_resources_1),
    reflexive("magazines", weap_magazine),
    reflexive("new_triggers", weap_new_trigger),
    reflexive("barrels", weap_barrel),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("maximum_movement_acceleration"),
    Float("maximum_movement_velocity"),
    Float("maximum_turning_acceleration"),
    Float("maximum_turning_velocity"),
    dependency("deployed_vehicle"),
    dependency("deployed_weapon"),
    dependency("age_model"),
    dependency("age_weapon"),
    dependency("aged_effect"),
    Float("hammer_age_per_use_mp"),
    Float("hammer_age_per_use_sp"),
    Float("first_person_weapon_offset_i"),
    Float("first_person_weapon_offset_j"),
    Float("first_person_weapon_offset_k"),
    Float("first_person_scope_size_i"),
    Float("first_person_scope_size_j"),
    Float("third_person_pitch_bounds_min"),
    Float("third_person_pitch_bounds_max"),
    Float("zoom_transition_time"),
    Float("melee_weapon_delay"),
    string_id_meta("weapon_holster_marker"),
    TYPE=Struct, ENDIAN=">", SIZE=1280
    )