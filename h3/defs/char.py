from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

char_general_propertie_actor_type = (
    "elite",
    "jackal",
    "grunt",
    "hunter",
    "engineer",
    "assassin",
    "player",
    "marine",
    "crew",
    "combat_form",
    "infection_form",
    "carrier_form",
    "monitor",
    "sentinel",
    "none",
    "mounted_weapon",
    "brute",
    "prophet",
    "bugger",
    "juggernaut",
    "pure_form_stealth",
    "pure_form_tank",
    "pure_form_ranged",
    "scarab",
    "guardian",
    )

char_grenades_propertie_grenade_type = (
    "frag",
    "plasma",
    "claymore",
    "firebomb",
    )

char_grenades_propertie_trajectory_type = (
    "toss",
    "lob",
    "bounce",
    )

char_metagame_propertie_classification = (
    "infantry",
    "leader",
    "hero",
    "specialist",
    "light_vehicle",
    "heavy_vehicle",
    "giant_vehicle",
    "standard_vehicle",
    )

char_metagame_propertie_unit = (
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

char_movement_propertie_jump_height = (
    "none",
    "down",
    "step",
    "crouch",
    "stand",
    "storey",
    "tower",
    "infinite",
    )

char_movement_propertie_obstace_leap_minimum_size = (
    "none",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "immobile",
    )

char_weapons_propertie_special_fire_mode = (
    "none",
    "overcharge",
    "secondary_trigger",
    )

char_weapons_propertie_special_fire_situation = (
    "never",
    "enemy_visible",
    "enemy_out_of_sight",
    "strafing",
    )


char_variant_dialogue_variation = Struct("dialogue_variations",
    dependency("dialogue"),
    string_id_meta("name"),
    Pad(4),
    ENDIAN=">", SIZE=24
    )


char_variant = Struct("variants",
    string_id_meta("variant_name"),
    SInt16("variant_index"),
    SInt16("unknown"),
    reflexive("dialogue_variations", char_variant_dialogue_variation),
    ENDIAN=">", SIZE=20
    )


char_unit_dialogue_dialogue_variation = Struct("dialogue_variations",
    dependency("dialogue"),
    string_id_meta("name"),
    Pad(4),
    ENDIAN=">", SIZE=24
    )


char_unit_dialogue = Struct("unit_dialogue",
    reflexive("dialogue_variations", char_unit_dialogue_dialogue_variation),
    ENDIAN=">", SIZE=12
    )


char_general_propertie = Struct("general_properties",
    Bool32("flags",
        "swarm",
        "flying",
        "dual_wields",
        "uses_gravemind",
        ("cannot_swap_weapons_with_player", 1 << 5),
        "does_not_initially_backpack",
        "revive_on_death",
        ),
    SEnum16("actor_type", *char_general_propertie_actor_type),
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    Pad(8),
    Float("scariness"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    ENDIAN=">", SIZE=28
    )


char_vitality_propertie = Struct("vitality_properties",
    Bool32("vitality_flags",
        "can_revive_on_death",
        ),
    Float("normal_body_vitality"),
    Float("normal_shield_vitality"),
    Float("legendary_body_vitality"),
    Float("legendary_shield_vitality"),
    Float("body_recharge_fraction"),
    Float("soft_ping_shield_threshold"),
    Float("soft_ping_noshield_threshold"),
    Float("soft_ping_minimum_interrupt_time"),
    Float("hard_ping_shield_threshold"),
    Float("hard_ping_noshield_threshold"),
    Float("hard_ping_minimum_interrupt_time"),
    Float("current_damage_decay_delay"),
    Float("current_damage_decay_time"),
    Float("recent_damage_decay_delay"),
    Float("recent_damage_decay_time"),
    Float("body_recharge_delay_time"),
    Float("body_recharge_time"),
    Float("shield_recharge_delay_time"),
    Float("shield_recharge_time"),
    Float("stun_threshold"),
    Float("stun_time_bounds_min"),
    Float("stun_time_bounds_max"),
    Float("extended_shield_damage_threshold"),
    Float("extended_body_damage_threshold"),
    Float("suicide_radius"),
    Float("unknown"),
    Float("unknown_1"),
    dependency("backup_weapon"),
    ENDIAN=">", SIZE=128
    )


char_placement_propertie = Struct("placement_properties",
    Pad(4),
    Float("few_upgrade_chance_easy"),
    Float("few_upgrade_chance_normal"),
    Float("few_upgrade_chance_heroic"),
    Float("few_upgrade_chance_legendary"),
    Float("normal_upgrade_chance_easy"),
    Float("normal_upgrade_chance_normal"),
    Float("normal_upgrade_chance_heroic"),
    Float("normal_upgrade_chance_legendary"),
    Float("many_upgrade_chance_easy"),
    Float("many_upgrade_chance_normal"),
    Float("many_upgrade_chance_heroic"),
    Float("many_upgrade_chance_legendary"),
    ENDIAN=">", SIZE=52
    )


char_perception_propertie = Struct("perception_properties",
    SInt32("perception_flags"),
    Float("max_vision_distance"),
    float_rad("central_vision_angle"),
    float_rad("max_vision_angle"),
    float_rad("peripheral_vision_angle"),
    Float("peripheral_distance"),
    Float("hearing_distance"),
    Float("notice_projectile_chance"),
    Float("notice_vehicle_chance"),
    Pad(4),
    Float("first_acknowledge_surprise_distance"),
    ENDIAN=">", SIZE=44
    )


char_look_propertie = Struct("look_properties",
    float_rad("maximum_aiming_deviation_y"),
    float_rad("maximum_aiming_deviation_p"),
    float_rad("maximum_looking_deviation_y"),
    float_rad("maximum_looking_deviation_p"),
    Pad(16),
    float_rad("noncombat_look_delta_l"),
    float_rad("noncombat_look_delta_r"),
    float_rad("combat_look_delta_l"),
    float_rad("combat_look_delta_r"),
    Float("noncombat_idle_looking_min"),
    Float("noncombat_idle_looking_max"),
    Float("noncombat_idle_aiming_min"),
    Float("noncombat_idle_aiming_max"),
    Float("combat_idle_looking_min"),
    Float("combat_idle_looking_max"),
    Float("combat_idle_aiming_min"),
    Float("combat_idle_aiming_max"),
    ENDIAN=">", SIZE=80
    )


char_movement_propertie = Struct("movement_properties",
    Bool32("movement_flags",
        ("prefer_to_combat_near_friends", 1 << 2),
        ),
    Float("pathfinding_radius"),
    Float("destination_radius"),
    Float("dive_grenade_chance"),
    SEnum16("obstace_leap_minimum_size", *char_movement_propertie_obstace_leap_minimum_size),
    SEnum16("obstace_leap_maximum_size", *char_movement_propertie_obstace_leap_minimum_size),
    SEnum16("obstace_ignore_size", *char_movement_propertie_obstace_leap_minimum_size),
    SEnum16("obstace_smashable_size", *char_movement_propertie_obstace_leap_minimum_size),
    SEnum32("jump_height", *char_movement_propertie_jump_height),
    Bool32("movement_hint_flags",
        ),
    Pad(12),
    ENDIAN=">", SIZE=44
    )


char_unknown = Struct("unknown",
    Pad(24),
    ENDIAN=">", SIZE=24
    )


char_swarm_propertie = Struct("swarm_properties",
    SInt16("scatter_killed_count"),
    SInt16("unknown"),
    Pad(8),
    Float("scatter_radius"),
    Float("scatter_distance"),
    Float("hound_min_distance"),
    Float("hound_max_distance"),
    Float("perlin_offset_scale"),
    Float("offset_period_min"),
    Float("offset_period_max"),
    Float("perlin_idle_movement_threshold"),
    Float("perlin_combat_movement_threshold"),
    Pad(8),
    ENDIAN=">", SIZE=56
    )


char_ready_propertie = Struct("ready_properties",
    Float("ready_time_bounds_min"),
    Float("ready_time_bounds_max"),
    ENDIAN=">", SIZE=8
    )


char_engage_propertie = Struct("engage_properties",
    Bool32("engage_flags",
        ),
    Pad(4),
    Float("crouch_danger_threshold"),
    Float("stand_danger_threshold"),
    Float("fight_danger_move_threshold"),
    Pad(4),
    dependency("unknown_2"),
    ENDIAN=">", SIZE=40
    )


char_charge_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=6
    )


char_charge_propertie = Struct("charge_properties",
    Bool32("charge_flags",
        "offhand_melee_allowed",
        ),
    Float("melee_consider_range"),
    Float("melee_chance"),
    Float("melee_attack_range"),
    Float("melee_abort_range"),
    Float("melee_attack_timeout"),
    Float("melee_attack_delay_timer"),
    Float("melee_leap_range_min"),
    Float("melee_leap_range_max"),
    Float("melee_leap_chance"),
    Float("ideal_leap_velocity"),
    Float("max_leap_velocity"),
    Float("melee_leap_ballistic"),
    Float("melee_delay_timer"),
    Pad(20),
    dependency("berserk_weapon"),
    Pad(20),
    reflexive("unknown_2", char_charge_propertie_unknown_2),
    ENDIAN=">", SIZE=124
    )


char_evasion_propertie = Struct("evasion_properties",
    Float("evasion_danger_threshold"),
    Float("evasion_delay_timer"),
    Float("evasion_chance"),
    Float("evasion_proximity_threshold"),
    Float("dive_retreat_chance"),
    ENDIAN=">", SIZE=20
    )


char_cover_propertie = Struct("cover_properties",
    Bool32("cover_flags",
        ),
    Float("hide_behind_cover_time_min"),
    Float("hide_behind_cover_time_max"),
    Float("cover_vitality_threshold"),
    Float("cover_shield_fraction"),
    Float("cover_check_delay"),
    Float("cover_danger_threshold"),
    Float("danger_upper_threshold"),
    Float("cover_chance_min"),
    Float("cover_chance_max"),
    Pad(12),
    Float("proximity_self_preserve"),
    Float("disallow_cover_distance"),
    Float("proximity_melee_distance"),
    Float("unreachable_enemy_danger_threashold"),
    Float("scary_target_threshold"),
    Pad(12),
    ENDIAN=">", SIZE=84
    )


char_retreat_propertie = Struct("retreat_properties",
    Bool32("retreat_flags",
        "zig_zag_when_fleeing",
        ),
    Float("shield_threshold"),
    Float("scary_target_threshold"),
    Float("danger_threshold"),
    Float("proximity_threshold"),
    Float("forced_cower_time_bounds_min"),
    Float("forced_cower_time_bounds_max"),
    Float("cower_time_bounds_min"),
    Float("cower_time_bounds_max"),
    Float("proximity_ambush_threshold"),
    Pad(20),
    float_rad("zig_zag_angle"),
    Float("zig_zag_period"),
    Float("retreat_grenade_chance"),
    dependency("backup_weapon"),
    ENDIAN=">", SIZE=88
    )


char_search_propertie = Struct("search_properties",
    Bool32("search_flags",
        ),
    Float("search_time_min"),
    Float("search_time_max"),
    Pad(4),
    Float("uncover_distance_bounds_min"),
    Float("uncover_distance_bounds_max"),
    Pad(8),
    ENDIAN=">", SIZE=32
    )


char_pre_search_propertie = Struct("pre_search_properties",
    Bool32("pre_search_flags",
        ),
    Float("minimum_presearch_time_min"),
    Float("minimum_presearch_time_max"),
    Float("maximum_presearch_time_min"),
    Float("maximum_presearch_time_max"),
    Float("minimum_certainty_radius"),
    Pad(4),
    Float("minimum_suppressing_time_min"),
    Float("minimum_suppressing_time_max"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=40
    )


char_idle_propertie = Struct("idle_properties",
    Pad(4),
    Float("idle_pose_delay_time_min"),
    Float("idle_pose_delay_time_max"),
    ENDIAN=">", SIZE=12
    )


char_vocalization_propertie = Struct("vocalization_properties",
    Pad(4),
    Float("look_comment_time"),
    Float("look_long_comment_time"),
    ENDIAN=">", SIZE=12
    )


char_boarding_propertie = Struct("boarding_properties",
    Bool32("flags",
        "airborne_boarding",
        ),
    Float("max_distance"),
    Float("abort_distance"),
    Float("max_speed"),
    Pad(4),
    ENDIAN=">", SIZE=20
    )


char_unknown_2 = Struct("unknown_2",
    Pad(8),
    ENDIAN=">", SIZE=8
    )


char_unknown_3 = Struct("unknown_3",
    Pad(24),
    ENDIAN=">", SIZE=24
    )


char_weapons_propertie_firing_pattern = Struct("firing_patterns",
    Float("rate_of_fire"),
    Float("target_tracking"),
    Float("target_leading"),
    Float("burst_origin_radius"),
    float_rad("burst_origin_angle"),
    Float("burst_return_length_min"),
    Float("burst_return_length_max"),
    float_rad("burst_return_angle"),
    Float("burst_duration_min"),
    Float("burst_duration_max"),
    Float("burst_separation_min"),
    Float("burst_separation_max"),
    Float("weapon_damage_modifier"),
    float_rad("projectile_error"),
    float_rad("burst_angular_velocity"),
    float_rad("maximum_error_angle"),
    ENDIAN=">", SIZE=64
    )


char_weapons_propertie = Struct("weapons_properties",
    Bool32("weapon_flags",
        ("must_crouch_to_shoot", 1 << 1),
        ),
    dependency("weapon"),
    Float("maximum_firing_range"),
    Float("minimum_firing_range"),
    Float("normal_combat_range_min"),
    Float("normal_combat_range_max"),
    Float("bombardment_range"),
    Float("max_special_target_distance"),
    Float("timid_combat_range_min"),
    Float("timid_combat_range_max"),
    Float("aggressive_combat_range_min"),
    Float("aggressive_combat_range_max"),
    Float("super_ballistic_range"),
    Float("ballistic_firing_bounds_min"),
    Float("ballistic_firing_bounds_max"),
    Float("ballistic_fraction_bounds_min"),
    Float("ballistic_fraction_bounds_max"),
    Float("first_burst_delay_time_min"),
    Float("first_burst_delay_time_max"),
    Float("surprise_delay_time"),
    Float("surprise_fire_wildly_time"),
    Float("death_fire_wildly_chance"),
    Float("death_fire_wildly_time"),
    Float("custom_stand_gun_offset_i"),
    Float("custom_stand_gun_offset_j"),
    Float("custom_stand_gun_offset_k"),
    Float("custom_crouch_gun_offset_i"),
    Float("custom_crouch_gun_offset_j"),
    Float("custom_crouch_gun_offset_k"),
    SEnum16("special_fire_mode", *char_weapons_propertie_special_fire_mode),
    SEnum16("special_fire_situation", *char_weapons_propertie_special_fire_situation),
    Float("special_fire_chance"),
    Float("special_fire_delay"),
    Float("special_damage_modifier"),
    float_rad("special_projectile_error"),
    Float("drop_weapon_loaded_min"),
    Float("drop_weapon_loaded_max"),
    SInt16("drop_weapon_ammo_min"),
    SInt16("drop_weapon_ammo_max"),
    Float("normal_accuracy_bounds_min"),
    Float("normal_accuracy_bounds_max"),
    Float("normal_accuracy_time"),
    Float("heroic_accuracy_bounds_min"),
    Float("heroic_accuracy_bounds_max"),
    Float("heroic_accuracy_time"),
    Float("legendary_accuracy_bounds_min"),
    Float("legendary_accuracy_bounds_max"),
    Float("legendary_accuracy_time"),
    reflexive("firing_patterns", char_weapons_propertie_firing_pattern),
    dependency("weapon_melee_damage"),
    ENDIAN=">", SIZE=224
    )


char_firing_pattern_propertie_firing_pattern = Struct("firing_patterns",
    Float("rate_of_fire"),
    Float("target_tracking"),
    Float("target_leading"),
    Float("burst_origin_radius"),
    float_rad("burst_origin_angle"),
    Float("burst_return_length_min"),
    Float("burst_return_length_max"),
    float_rad("burst_return_angle"),
    Float("burst_duration_min"),
    Float("burst_duration_max"),
    Float("burst_separation_min"),
    Float("burst_separation_max"),
    Float("weapon_damage_modifier"),
    float_rad("projectile_error"),
    float_rad("burst_angular_velocity"),
    float_rad("maximum_error_angle"),
    ENDIAN=">", SIZE=64
    )


char_firing_pattern_propertie = Struct("firing_pattern_properties",
    dependency("weapon"),
    reflexive("firing_patterns", char_firing_pattern_propertie_firing_pattern),
    ENDIAN=">", SIZE=28
    )


char_grenades_propertie = Struct("grenades_properties",
    SInt32("grenades_flags"),
    SEnum16("grenade_type", *char_grenades_propertie_grenade_type),
    SEnum16("trajectory_type", *char_grenades_propertie_trajectory_type),
    SInt32("minimum_enemy_count"),
    Float("enemy_radius"),
    Float("grenade_ideal_velocity"),
    Float("grenade_velocity"),
    Float("grenade_range_min"),
    Float("grenade_range_max"),
    Float("collateral_damage_radius"),
    Float("grenade_chance"),
    Float("grenade_throw_delay"),
    Float("grenade_uncover_chance"),
    Float("anti_vehicle_grenade_chance"),
    SInt16("dropped_grenade_count_min"),
    SInt16("dropped_grenade_count_max"),
    Float("don_t_drop_grenades_chance"),
    ENDIAN=">", SIZE=60
    )


char_vehicle_propertie = Struct("vehicle_properties",
    dependency("unit"),
    dependency("style"),
    Bool32("vehicle_flags",
        "passengers_adopt_original_squad",
        ),
    Float("ai_pathfinding_radius"),
    Float("ai_destination_radius"),
    Float("ai_deceleration_distance"),
    Float("ai_turning_radius"),
    Float("ai_inner_turning_radius"),
    Float("ai_ideal_turning_radius"),
    float_rad("ai_banshee_steering_maximum"),
    Float("ai_max_steering_angle"),
    Float("ai_max_steering_delta"),
    Float("ai_oversteering_scale"),
    float_rad("ai_oversteering_bounds_min"),
    float_rad("ai_oversteering_bounds_max"),
    Float("ai_side_slip_distance"),
    Float("ai_avoidance_distance"),
    Float("ai_minimum_urgency"),
    float_rad("unknown"),
    Pad(4),
    Float("ai_throttle_maximum"),
    Float("ai_goal_minimum_throttle_scale"),
    Float("ai_turn_minimum_throttle_scale"),
    Float("ai_direction_minimum_throttle_scale"),
    Float("ai_acceleration_scale"),
    Float("ai_throttle_blend"),
    Float("theoretical_max_speed"),
    Float("error_scale"),
    float_rad("ai_allowable_aim_deviation_angle"),
    Float("ai_charge_tight_angle_distance"),
    Float("ai_charge_tight_angle"),
    Float("ai_charge_repeat_timeout"),
    Float("ai_charge_look_ahead_time"),
    Float("ai_consider_distance"),
    Float("ai_charge_abort_distance"),
    Float("vehicle_ram_timeout"),
    Float("ram_paralysis_time"),
    Float("ai_cover_damage_threshold"),
    Float("ai_cover_minimum_distance"),
    Float("ai_cover_time"),
    Float("ai_cover_minimum_boost_distance"),
    Float("turtling_recent_damage_threshold"),
    Float("turtling_minimum_time"),
    Float("turtling_timeout"),
    SEnum16("obstacle_ignore_size", *char_movement_propertie_obstace_leap_minimum_size),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=208
    )


char_morph_propertie = Struct("morph_properties",
    dependency("morph_character_1"),
    dependency("morph_character_2"),
    dependency("morph_character_3"),
    dependency("morph_muffin"),
    dependency("morph_weapon_1"),
    dependency("morph_weapon_2"),
    dependency("morph_weapon_3"),
    Pad(32),
    dependency("character"),
    Pad(4),
    string_id_meta("unknown_2"),
    Pad(60),
    ENDIAN=">", SIZE=228
    )


char_equipment_propertie_usage_condition = Struct("usage_conditions",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    ENDIAN=">", SIZE=12
    )


char_equipment_propertie = Struct("equipment_properties",
    dependency("equipment"),
    Pad(4),
    Float("usage_chance"),
    reflexive("usage_conditions", char_equipment_propertie_usage_condition),
    ENDIAN=">", SIZE=36
    )


char_metagame_propertie = Struct("metagame_properties",
    Bool8("flags",
        "must_have_active_seats",
        ),
    SEnum8("unit", *char_metagame_propertie_unit),
    SEnum8("classification", *char_metagame_propertie_classification),
    SInt8("unknown"),
    SInt16("points"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=8
    )


char_act_attachment = Struct("act_attachments",
    string_id_meta("name"),
    dependency("child_object"),
    string_id_meta("child_marker"),
    string_id_meta("parent_marker"),
    ENDIAN=">", SIZE=28
    )


char_meta_def = BlockDef("char",
    Bool32("character_flags",
        ),
    dependency("parent_character"),
    dependency("unit"),
    dependency("creature"),
    dependency("style"),
    dependency("major_character"),
    reflexive("variants", char_variant),
    reflexive("unit_dialogue", char_unit_dialogue),
    reflexive("general_properties", char_general_propertie),
    reflexive("vitality_properties", char_vitality_propertie),
    reflexive("placement_properties", char_placement_propertie),
    reflexive("perception_properties", char_perception_propertie),
    reflexive("look_properties", char_look_propertie),
    reflexive("movement_properties", char_movement_propertie),
    reflexive("unknown", char_unknown),
    reflexive("swarm_properties", char_swarm_propertie),
    reflexive("ready_properties", char_ready_propertie),
    reflexive("engage_properties", char_engage_propertie),
    reflexive("charge_properties", char_charge_propertie),
    reflexive("evasion_properties", char_evasion_propertie),
    reflexive("cover_properties", char_cover_propertie),
    reflexive("retreat_properties", char_retreat_propertie),
    reflexive("search_properties", char_search_propertie),
    reflexive("pre_search_properties", char_pre_search_propertie),
    reflexive("idle_properties", char_idle_propertie),
    reflexive("vocalization_properties", char_vocalization_propertie),
    reflexive("boarding_properties", char_boarding_propertie),
    Pad(12),
    reflexive("unknown_2", char_unknown_2),
    reflexive("unknown_3", char_unknown_3),
    reflexive("weapons_properties", char_weapons_propertie),
    reflexive("firing_pattern_properties", char_firing_pattern_propertie),
    reflexive("grenades_properties", char_grenades_propertie),
    reflexive("vehicle_properties", char_vehicle_propertie),
    reflexive("morph_properties", char_morph_propertie),
    reflexive("equipment_properties", char_equipment_propertie),
    reflexive("metagame_properties", char_metagame_propertie),
    reflexive("act_attachments", char_act_attachment),
    TYPE=Struct, ENDIAN=">", SIZE=468
    )