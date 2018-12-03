############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Veegie
# 	Mapped out reflextives and idents. Fixed titles.
# revision: 3		author: DarkShallFall
# 	Mapped out some values in barrel, new triggers, etc.
# revision: 4		author: DarkShallFall
# 	Mapped out and labeled all of the "Firing Effect" reflexive.
# revision: 5		author: DeadCanadian
# 	fixed third person flag, and named sounds
# revision: 6		author: Lord Zedd
# 	Portin'
# revision: 7		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

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

weap_barrel_prediction_type = (
    "none",
    "continuous",
    "instant",
    )

weap_movement_penalized = (
    "always",
    "when_zoomed",
    "when_zoomed_or_reloading",
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

weap_secondary_trigger_mode = (
    "normal",
    "slaved_to_primary",
    "inhibits_primary",
    "loads_alternate_ammunition",
    "loads_multiple_primary_ammunition",
    )

weap_tracking_type = (
    "no_tracking",
    "human_tracking",
    "plasma_tracking",
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


weap_early_mover_propertie = Struct("early_mover_propertie", 
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


weap_ai_propertie = Struct("ai_propertie", 
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


weap_function = Struct("function", 
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


weap_attachment = Struct("attachment", 
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


weap_widget = Struct("widget", 
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


weap_change_color_initial_permutation = Struct("initial_permutation", 
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


weap_change_color_function = Struct("function", 
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


weap_change_color = Struct("change_color", 
    h3_reflexive("initial_permutations", weap_change_color_initial_permutation),
    h3_reflexive("functions", weap_change_color_function),
    ENDIAN=">", SIZE=24
    )


weap_predicted_resources_0 = Struct("predicted_resources_0", 
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


weap_multiplayer_object_propertie = Struct("multiplayer_object_propertie", 
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


weap_predicted_bitmap = Struct("predicted_bitmap", 
    h3_dependency("bitmap", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


weap_first_person = Struct("first_person", 
    h3_dependency("first_person_model"),
    h3_dependency("first_person_animations"),
    ENDIAN=">", SIZE=32
    )


weap_predicted_resources_1 = Struct("predicted_resources_1", 
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


weap_magazine_magazine_equipment = Struct("magazine_equipment", 
    SInt16("rounds_0_for_max"),
    SInt16("unknown", VISIBLE=False),
    h3_dependency("equipment"),
    ENDIAN=">", SIZE=20
    )


weap_magazine = Struct("magazine", 
    Bool32("flags", 
        "wastes_rounds_when_reloaded",
        "every_round_must_be_chambered",
        ),
    SInt16("rounds_recharged"),
    SInt16("rounds_total_initial"),
    SInt16("rounds_total_maximum"),
    SInt16("rounds_total_loaded_maximum"),
    SInt16("maximum_rounds_held"),
    SInt16("unknown_0"),
    Float("reload_time"),
    SInt16("rounds_reloaded"),
    SInt16("unknown_1", VISIBLE=False),
    Float("chamber_time"),
    BytesRaw("unknown_2", SIZE=24, VISIBLE=False),
    h3_dependency("reloading_effect"),
    h3_dependency("reloading_damage_effect"),
    h3_dependency("chambering_effect"),
    h3_dependency("chambering_damage_effect"),
    h3_reflexive("magazine_equipment", weap_magazine_magazine_equipment),
    ENDIAN=">", SIZE=128
    )


weap_new_trigger = Struct("new_trigger", 
    Bool32("flags", 
        "autofire_single_action_only",
        ),
    SEnum16("button_used", *weap_new_trigger_button_used),
    SEnum16("behavior", *weap_new_trigger_behavior),
    SInt16("primary_barrel"),
    SInt16("secondary_barrel"),
    SEnum16("prediction", *weap_new_trigger_prediction),
    SInt16("unknown_0", VISIBLE=False),
    Float("autofire_time"),
    Float("autofire_throw"),
    SEnum16("secondary_action", *weap_new_trigger_secondary_action),
    SEnum16("primary_action", *weap_new_trigger_secondary_action),
    Float("charging_time"),
    Float("charged_time"),
    SEnum16("overcharge_action", *weap_new_trigger_overcharge_action),
    Bool16("charge_flags", *unknown_flags_16),
    Float("charged_illumination"),
    Float("spew_time"),
    h3_dependency("charging_effect"),
    h3_dependency("charging_damage_effect"),
    h3_dependency("charging_response"),
    Float("charging_age_degeneration"),
    h3_dependency("discharging_effect"),
    h3_dependency("discharging_damage_effect"),
    Float("target_tracking_decay_time"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=144
    )


weap_barrel_first_person_offset = Struct("first_person_offset", 
    QStruct("first_person_offset", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=12
    )


weap_barrel_firing_effect = Struct("firing_effect", 
    SInt16("shot_count_lower_bound"),
    SInt16("shot_count_upper_bound"),
    h3_dependency("firing_effect"),
    h3_dependency("misfire_effect"),
    h3_dependency("empty_effect"),
    h3_dependency("unknown_effect"),
    h3_dependency("firing_response"),
    h3_dependency("misfire_response"),
    h3_dependency("empty_response"),
    h3_dependency("unknown_response"),
    h3_dependency("rider_firing_response"),
    h3_dependency("rider_misfire_response"),
    h3_dependency("rider_empty_response"),
    h3_dependency("rider_unknown_response"),
    ENDIAN=">", SIZE=196
    )


weap_barrel = Struct("barrel", 
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
        "dont_clear_fire_bit_after_recovering",
        "stagger_fire_across_multiple_markers",
        "fires_locked_projectiles",
        ),
    QStruct("rounds_per_second", INCLUDE=from_to),
    Float("acceleration_time_0"),
    Float("deceleration_time_0"),
    Float("barrel_spin_scale"),
    Float("blurred_rate_of_fire"),
    QStruct("shots_per_fire", INCLUDE=from_to_sint16),
    Float("fire_recovery_time"),
    Float("soft_recovery_fraction"),
    SInt16("magazine"),
    SInt16("rounds_per_shot"),
    SInt16("minimum_rounds_loaded"),
    SInt16("rounds_between_tracers"),
    h3_string_id("optional_barrel_marker_name"),
    SEnum16("prediction_type", *weap_barrel_prediction_type),
    SEnum16("firing_noise", *gint_constant_sound_volume),
    Float("acceleration_time_1"),
    Float("deceleration_time_1"),
    QStruct("damage_error", INCLUDE=from_to),
    float_rad("base_turning_speed"),
    from_to_rad("dynamic_turning_speed"),
    Float("acceleration_time_2"),
    Float("deceleration_time_2"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    float_rad("minimum_error_0"),
    from_to_rad("error_angle_0"),
    Float("dual_wield_damage_scale"),
    SEnum16("distribution_function", *weap_barrel_distribution_function),
    SInt16("projectiles_per_shot"),
    float_rad("distribution_angle"),
    float_rad("minimum_error_1"),
    from_to_rad("error_angle_1"),
    h3_reflexive("first_person_offsets", weap_barrel_first_person_offset),
    SEnum8("damage_reporting_type", *proj_damage_reporting_type),
    SInt8("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("initial_projectile"),
    h3_dependency("trailing_projectile"),
    h3_dependency("damage_effect"),
    h3_dependency("crate_projectile"),
    Float("crate_projectile_speed"),
    Float("ejection_port_recovery_time"),
    Float("illumination_recovery_time"),
    Float("heat_generated_per_round"),
    Float("age_generated_per_round_mp"),
    Float("age_generated_per_round_sp"),
    Float("overload_time"),
    from_to_rad("angle_change_per_shot"),
    Pad(8),
    SEnum16("angle_change_function", *weap_barrel_angle_change_function),
    SInt16("unknown_4", VISIBLE=False),
    Float("unknown_5", VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    Float("firing_effect_deceleration_time"),
    Float("unknown_7", VISIBLE=False),
    Float("rate_of_fire_acceleration_time"),
    Float("rate_of_fire_deceleration_time"),
    Float("unknown_8", VISIBLE=False),
    Float("unknown_9", VISIBLE=False),
    h3_reflexive("firing_effects", weap_barrel_firing_effect),
    ENDIAN=">", SIZE=308
    )


weap_body = Struct("tagdata", 
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
    h3_reflexive("early_mover_properties", weap_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", weap_ai_propertie),
    h3_reflexive("functions", weap_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", weap_attachment),
    h3_reflexive("widgets", weap_widget),
    h3_reflexive("change_colors", weap_change_color),
    h3_reflexive("predicted_resources_0", weap_predicted_resources_0),
    h3_reflexive("multiplayer_object_properties", weap_multiplayer_object_propertie),
    Bool32("flags_1", 
        "always_maintains_z_up",
        "destroyed_by_explosions",
        "unaffected_by_gravity",
        ),
    SInt16("old_message_index"),
    SInt16("sort_order"),
    Float("old_multiplayer_on_ground_scale"),
    Float("old_campaign_on_ground_scale"),
    h3_string_id("pickup_message"),
    h3_string_id("swap_message"),
    h3_string_id("pickup_or_dual_wield_message"),
    h3_string_id("swap_or_dual_wield_message"),
    h3_string_id("picked_up_message"),
    h3_string_id("switch_to_message"),
    h3_string_id("switch_to_from_ai_message"),
    h3_string_id("all_weapons_empty_message"),
    h3_dependency("collision_sound"),
    h3_reflexive("predicted_bitmaps", weap_predicted_bitmap),
    h3_dependency("detonation_damage_effect_0"),
    QStruct("detonation_delay", INCLUDE=from_to),
    h3_dependency("detonating_effect"),
    h3_dependency("detonation_effect"),
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
    Bool32("more_flags", *unknown_flags_32),
    h3_string_id("unknown_2"),
    SEnum16("secondary_trigger_mode", *weap_secondary_trigger_mode),
    SInt16("maximum_alternate_shots_loaded"),
    Float("turn_on_time"),
    Float("ready_time"),
    h3_dependency("ready_effect"),
    h3_dependency("ready_damage_effect"),
    Float("heat_recovery_threshold"),
    Float("overheated_threshold"),
    Float("heat_detonation_threshold"),
    Float("heat_detonation_fraction"),
    Float("heat_loss_per_second"),
    Float("heat_illumination"),
    Float("overheated_heat_loss_per_second"),
    h3_dependency("overheated"),
    h3_dependency("overheated_damage_effect"),
    h3_dependency("detonation"),
    h3_dependency("detonation_damage_effect_1"),
    h3_dependency("player_melee_damage"),
    h3_dependency("player_melee_response"),
    yp_float_rad("damage_pyramid_angles"),
    Float("damage_pyramid_depth"),
    h3_dependency("_1st_hit_damage"),
    h3_dependency("_1st_hit_response"),
    h3_dependency("_2nd_hit_damage"),
    h3_dependency("_2nd_hit_response"),
    h3_dependency("_3rd_hit_damage"),
    h3_dependency("_3rd_hit_response"),
    h3_dependency("lunge_melee_damage"),
    h3_dependency("lunge_melee_response"),
    h3_dependency("gun_gun_clang_damage"),
    h3_dependency("gun_gun_clang_response"),
    h3_dependency("gun_sword_clang_damage"),
    h3_dependency("gun_sword_clang_response"),
    h3_dependency("clash_effect"),
    SEnum8("melee_damage_reporting_type", *proj_damage_reporting_type),
    SInt8("unknown_3", VISIBLE=False),
    SInt16("magnification_levels"),
    QStruct("magnification_range", INCLUDE=from_to),
    float_rad("autoaim_angle"),
    Float("autoaim_range_long"),
    Float("autoaim_range_short"),
    float_rad("magnetism_angle"),
    Float("magnetism_range_long"),
    Float("magnetism_range_short"),
    float_rad("deviation_angle"),
    BytesRaw("unknown_4", SIZE=20, VISIBLE=False),
    SEnum16("movement_penalized", *weap_movement_penalized),
    SInt16("unknown_5", VISIBLE=False),
    Float("forwards_movement_penalty"),
    Float("sideways_movement_penalty"),
    Float("ai_scariness"),
    Float("weapon_power_on_time"),
    Float("weapon_power_off_time"),
    h3_dependency("weapon_power_on_effect"),
    h3_dependency("weapon_power_off_effect"),
    Float("age_heat_recovery_penalty"),
    Float("age_rate_of_fire_penalty"),
    Float("age_misfire_start"),
    Float("age_misfire_chance"),
    h3_dependency("pickup_sound"),
    h3_dependency("zoom_in_sound"),
    h3_dependency("zoom_out_sound"),
    Float("active_camo_ding"),
    Float("active_camo_regrowth_rate"),
    h3_string_id("handle_node"),
    h3_string_id("weapon_class"),
    h3_string_id("weapon_name"),
    SEnum16("multiplayer_weapon_type", *weap_multiplayer_weapon_type),
    SEnum16("weapon_type", *weap_weapon_type),
    SEnum16("tracking_type", *weap_tracking_type),
    SInt16("unknown_6", VISIBLE=False),
    BytesRaw("unknown_7", SIZE=16, VISIBLE=False),
    h3_reflexive("first_person", weap_first_person),
    h3_dependency("hud_interface"),
    h3_reflexive("predicted_resources_1", weap_predicted_resources_1),
    h3_reflexive("magazines", weap_magazine),
    h3_reflexive("new_triggers", weap_new_trigger),
    h3_reflexive("barrels", weap_barrel),
    Float("unknown_8", VISIBLE=False),
    Float("unknown_9", VISIBLE=False),
    Float("maximum_movement_acceleration"),
    Float("maximum_movement_velocity"),
    Float("maximum_turning_acceleration"),
    Float("maximum_turning_velocity"),
    h3_dependency("deployed_vehicle"),
    h3_dependency("deployed_weapon"),
    h3_dependency("age_model"),
    h3_dependency("age_weapon"),
    h3_dependency("aged_effect"),
    Float("hammer_age_per_use_mp"),
    Float("hammer_age_per_use_sp"),
    QStruct("first_person_weapon_offset", INCLUDE=ijk_float),
    QStruct("first_person_scope_size", INCLUDE=ij_float),
    QStruct("third_person_pitch_bounds", INCLUDE=from_to),
    Float("zoom_transition_time"),
    Float("melee_weapon_delay"),
    h3_string_id("weapon_holster_marker"),
    ENDIAN=">", SIZE=1280
    )


def get():
    return weap_def

weap_def = TagDef("weap",
    h3_blam_header('weap'),
    weap_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["weap"], endian=">", tag_cls=H3Tag
    )