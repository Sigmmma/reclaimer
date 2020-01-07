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
# 	Mapped some value names.
# revision: 3		author: DeadCanadian
# 	Mapped some value names.
# revision: 4		author: Lord Zedd
# 	Updated and standardized.
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
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


char_variant_dialogue_variation = Struct("dialogue_variation",
    h3_dependency("dialogue"),
    h3_string_id("name"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


char_variant = Struct("variant",
    h3_string_id("variant_name"),
    SInt16("variant_index"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("dialogue_variations", char_variant_dialogue_variation),
    ENDIAN=">", SIZE=20
    )


char_unit_dialogue_dialogue_variation = Struct("dialogue_variation",
    h3_dependency("dialogue"),
    h3_string_id("name"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


char_unit_dialogue = Struct("unit_dialogue",
    h3_reflexive("dialogue_variations", char_unit_dialogue_dialogue_variation),
    ENDIAN=">", SIZE=12
    )


char_general_propertie = Struct("general_propertie",
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
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=8, VISIBLE=False),
    Float("scariness"),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("unknown_5", VISIBLE=False),
    ENDIAN=">", SIZE=28
    )


char_vitality_propertie = Struct("vitality_propertie",
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
    QStruct("stun_time_bounds", INCLUDE=from_to),
    Float("extended_shield_damage_threshold"),
    Float("extended_body_damage_threshold"),
    Float("suicide_radius"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    h3_dependency("backup_weapon"),
    ENDIAN=">", SIZE=128
    )


char_placement_propertie = Struct("placement_propertie",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
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


char_perception_propertie = Struct("perception_propertie",
    SInt32("perception_flags"),
    Float("max_vision_distance"),
    float_rad("central_vision_angle"),
    float_rad("max_vision_angle"),
    float_rad("peripheral_vision_angle"),
    Float("peripheral_distance"),
    Float("hearing_distance"),
    Float("notice_projectile_chance"),
    Float("notice_vehicle_chance"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    Float("first_acknowledge_surprise_distance"),
    ENDIAN=">", SIZE=44
    )


char_look_propertie = Struct("look_propertie",
    yp_float_rad("maximum_aiming_deviation"),
    yp_float_rad("maximum_looking_deviation"),
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    float_rad("noncombat_look_delta_l"),
    float_rad("noncombat_look_delta_r"),
    float_rad("combat_look_delta_l"),
    float_rad("combat_look_delta_r"),
    QStruct("noncombat_idle_looking", INCLUDE=from_to),
    QStruct("noncombat_idle_aiming", INCLUDE=from_to),
    QStruct("combat_idle_looking", INCLUDE=from_to),
    QStruct("combat_idle_aiming", INCLUDE=from_to),
    ENDIAN=">", SIZE=80
    )


char_movement_propertie = Struct("movement_propertie",
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
    SEnum32("jump_height", *bloc_ai_propertie_leap_jump_speed),
    Bool32("movement_hint_flags", *unknown_flags_32),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=44
    )


char_unknown_0 = Struct("unknown_0",
    BytesRaw("unknown", SIZE=24, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


char_swarm_propertie = Struct("swarm_propertie",
    SInt16("scatter_killed_count"),
    SInt16("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    Float("scatter_radius"),
    Float("scatter_distance"),
    Float("hound_min_distance"),
    Float("hound_max_distance"),
    Float("perlin_offset_scale"),
    QStruct("offset_period", INCLUDE=from_to),
    Float("perlin_idle_movement_threshold"),
    Float("perlin_combat_movement_threshold"),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=56
    )


char_ready_propertie = Struct("ready_propertie",
    QStruct("ready_time_bounds", INCLUDE=from_to),
    ENDIAN=">", SIZE=8
    )


char_engage_propertie = Struct("engage_propertie",
    Bool32("engage_flags", *unknown_flags_32),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("crouch_danger_threshold"),
    Float("stand_danger_threshold"),
    Float("fight_danger_move_threshold"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_dependency("unknown_2"),
    ENDIAN=">", SIZE=40
    )


char_charge_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=6
    )


char_charge_propertie = Struct("charge_propertie",
    Bool32("charge_flags",
        "offhand_melee_allowed",
        ),
    Float("melee_consider_range"),
    Float("melee_chance"),
    Float("melee_attack_range"),
    Float("melee_abort_range"),
    Float("melee_attack_timeout"),
    Float("melee_attack_delay_timer"),
    QStruct("melee_leap_range", INCLUDE=from_to),
    Float("melee_leap_chance"),
    Float("ideal_leap_velocity"),
    Float("max_leap_velocity"),
    Float("melee_leap_ballistic"),
    Float("melee_delay_timer"),
    BytesRaw("unknown_0", SIZE=20, VISIBLE=False),
    h3_dependency("berserk_weapon"),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_reflexive("unknown_2", char_charge_propertie_unknown_2),
    ENDIAN=">", SIZE=124
    )


char_evasion_propertie = Struct("evasion_propertie",
    Float("evasion_danger_threshold"),
    Float("evasion_delay_timer"),
    Float("evasion_chance"),
    Float("evasion_proximity_threshold"),
    Float("dive_retreat_chance"),
    ENDIAN=">", SIZE=20
    )


char_cover_propertie = Struct("cover_propertie",
    Bool32("cover_flags", *unknown_flags_32),
    QStruct("hide_behind_cover_time", INCLUDE=from_to),
    Float("cover_vitality_threshold"),
    Float("cover_shield_fraction"),
    Float("cover_check_delay"),
    Float("cover_danger_threshold"),
    Float("danger_upper_threshold"),
    QStruct("cover_chance", INCLUDE=from_to),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    Float("proximity_self_preserve"),
    Float("disallow_cover_distance"),
    Float("proximity_melee_distance"),
    Float("unreachable_enemy_danger_threashold"),
    Float("scary_target_threshold"),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=84
    )


char_retreat_propertie = Struct("retreat_propertie",
    Bool32("retreat_flags",
        "zig_zag_when_fleeing",
        ),
    Float("shield_threshold"),
    Float("scary_target_threshold"),
    Float("danger_threshold"),
    Float("proximity_threshold"),
    QStruct("forced_cower_time_bounds", INCLUDE=from_to),
    QStruct("cower_time_bounds", INCLUDE=from_to),
    Float("proximity_ambush_threshold"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    float_rad("zig_zag_angle"),
    Float("zig_zag_period"),
    Float("retreat_grenade_chance"),
    h3_dependency("backup_weapon"),
    ENDIAN=">", SIZE=88
    )


char_search_propertie = Struct("search_propertie",
    Bool32("search_flags", *unknown_flags_32),
    QStruct("search_time", INCLUDE=from_to),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    QStruct("uncover_distance_bounds", INCLUDE=from_to),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


char_pre_search_propertie = Struct("pre_search_propertie",
    Bool32("pre_search_flags", *unknown_flags_32),
    QStruct("minimum_presearch_time", INCLUDE=from_to),
    QStruct("maximum_presearch_time", INCLUDE=from_to),
    Float("minimum_certainty_radius"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    QStruct("minimum_suppressing_time", INCLUDE=from_to),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=40
    )


char_idle_propertie = Struct("idle_propertie",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    QStruct("idle_pose_delay_time", INCLUDE=from_to),
    ENDIAN=">", SIZE=12
    )


char_vocalization_propertie = Struct("vocalization_propertie",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    Float("look_comment_time"),
    Float("look_long_comment_time"),
    ENDIAN=">", SIZE=12
    )


char_boarding_propertie = Struct("boarding_propertie",
    Bool32("flags",
        "airborne_boarding",
        ),
    Float("max_distance"),
    Float("abort_distance"),
    Float("max_speed"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


char_unknown_2 = Struct("unknown_2",
    BytesRaw("unknown", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


char_unknown_3 = Struct("unknown_3",
    BytesRaw("unknown", SIZE=24, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


char_weapons_propertie_firing_pattern = Struct("firing_pattern",
    Float("rate_of_fire"),
    Float("target_tracking"),
    Float("target_leading"),
    Float("burst_origin_radius"),
    float_rad("burst_origin_angle"),
    QStruct("burst_return_length", INCLUDE=from_to),
    float_rad("burst_return_angle"),
    QStruct("burst_duration", INCLUDE=from_to),
    QStruct("burst_separation", INCLUDE=from_to),
    Float("weapon_damage_modifier"),
    float_rad("projectile_error"),
    float_rad("burst_angular_velocity"),
    float_rad("maximum_error_angle"),
    ENDIAN=">", SIZE=64
    )


char_weapons_propertie = Struct("weapons_propertie",
    Bool32("weapon_flags",
        ("must_crouch_to_shoot", 1 << 1),
        ),
    h3_dependency("weapon"),
    Float("maximum_firing_range"),
    Float("minimum_firing_range"),
    QStruct("normal_combat_range", INCLUDE=from_to),
    Float("bombardment_range"),
    Float("max_special_target_distance"),
    QStruct("timid_combat_range", INCLUDE=from_to),
    QStruct("aggressive_combat_range", INCLUDE=from_to),
    Float("super_ballistic_range"),
    QStruct("ballistic_firing_bounds", INCLUDE=from_to),
    QStruct("ballistic_fraction_bounds", INCLUDE=from_to),
    QStruct("first_burst_delay_time", INCLUDE=from_to),
    Float("surprise_delay_time"),
    Float("surprise_fire_wildly_time"),
    Float("death_fire_wildly_chance"),
    Float("death_fire_wildly_time"),
    QStruct("custom_stand_gun_offset", INCLUDE=ijk_float),
    QStruct("custom_crouch_gun_offset", INCLUDE=ijk_float),
    SEnum16("special_fire_mode", *char_weapons_propertie_special_fire_mode),
    SEnum16("special_fire_situation", *char_weapons_propertie_special_fire_situation),
    Float("special_fire_chance"),
    Float("special_fire_delay"),
    Float("special_damage_modifier"),
    float_rad("special_projectile_error"),
    QStruct("drop_weapon_loaded", INCLUDE=from_to),
    QStruct("drop_weapon_ammo", INCLUDE=from_to_sint16),
    QStruct("normal_accuracy_bounds", INCLUDE=from_to),
    Float("normal_accuracy_time"),
    QStruct("heroic_accuracy_bounds", INCLUDE=from_to),
    Float("heroic_accuracy_time"),
    QStruct("legendary_accuracy_bounds", INCLUDE=from_to),
    Float("legendary_accuracy_time"),
    h3_reflexive("firing_patterns", char_weapons_propertie_firing_pattern),
    h3_dependency("weapon_melee_damage"),
    ENDIAN=">", SIZE=224
    )


char_firing_pattern_propertie_firing_pattern = Struct("firing_pattern",
    Float("rate_of_fire"),
    Float("target_tracking"),
    Float("target_leading"),
    Float("burst_origin_radius"),
    float_rad("burst_origin_angle"),
    QStruct("burst_return_length", INCLUDE=from_to),
    float_rad("burst_return_angle"),
    QStruct("burst_duration", INCLUDE=from_to),
    QStruct("burst_separation", INCLUDE=from_to),
    Float("weapon_damage_modifier"),
    float_rad("projectile_error"),
    float_rad("burst_angular_velocity"),
    float_rad("maximum_error_angle"),
    ENDIAN=">", SIZE=64
    )


char_firing_pattern_propertie = Struct("firing_pattern_propertie",
    h3_dependency("weapon"),
    h3_reflexive("firing_patterns", char_firing_pattern_propertie_firing_pattern),
    ENDIAN=">", SIZE=28
    )


char_grenades_propertie = Struct("grenades_propertie",
    SInt32("grenades_flags"),
    SEnum16("grenade_type", *char_grenades_propertie_grenade_type),
    SEnum16("trajectory_type", *char_grenades_propertie_trajectory_type),
    SInt32("minimum_enemy_count"),
    Float("enemy_radius"),
    Float("grenade_ideal_velocity"),
    Float("grenade_velocity"),
    QStruct("grenade_range", INCLUDE=from_to),
    Float("collateral_damage_radius"),
    Float("grenade_chance"),
    Float("grenade_throw_delay"),
    Float("grenade_uncover_chance"),
    Float("anti_vehicle_grenade_chance"),
    QStruct("dropped_grenade_count", INCLUDE=from_to_sint16),
    Float("dont_drop_grenades_chance"),
    ENDIAN=">", SIZE=60
    )


char_vehicle_propertie = Struct("vehicle_propertie",
    h3_dependency("unit"),
    h3_dependency("style"),
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
    from_to_rad("ai_oversteering_bounds"),
    Float("ai_side_slip_distance"),
    Float("ai_avoidance_distance"),
    Float("ai_minimum_urgency"),
    float_rad("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
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
    SInt16("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    ENDIAN=">", SIZE=208
    )


char_morph_propertie = Struct("morph_propertie",
    h3_dependency("morph_character_1"),
    h3_dependency("morph_character_2"),
    h3_dependency("morph_character_3"),
    h3_dependency("morph_muffin"),
    h3_dependency("morph_weapon_1"),
    h3_dependency("morph_weapon_2"),
    h3_dependency("morph_weapon_3"),
    BytesRaw("unknown_0", SIZE=32, VISIBLE=False),
    h3_dependency("character"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_string_id("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=60, VISIBLE=False),
    ENDIAN=">", SIZE=228
    )


char_equipment_propertie_usage_condition = Struct("usage_condition",
    SInt16("unknown_0"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    ENDIAN=">", SIZE=12
    )


char_equipment_propertie = Struct("equipment_propertie",
    h3_dependency("equipment"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    Float("usage_chance"),
    h3_reflexive("usage_conditions", char_equipment_propertie_usage_condition),
    ENDIAN=">", SIZE=36
    )


char_metagame_propertie = Struct("metagame_propertie",
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


char_act_attachment = Struct("act_attachment",
    h3_string_id("name"),
    h3_dependency("child_object"),
    h3_string_id("child_marker"),
    h3_string_id("parent_marker"),
    ENDIAN=">", SIZE=28
    )


char_body = Struct("tagdata",
    Bool32("character_flags", *unknown_flags_32),
    h3_dependency("parent_character"),
    h3_dependency("unit"),
    h3_dependency("creature"),
    h3_dependency("style"),
    h3_dependency("major_character"),
    h3_reflexive("variants", char_variant),
    h3_reflexive("unit_dialogue", char_unit_dialogue),
    h3_reflexive("general_properties", char_general_propertie),
    h3_reflexive("vitality_properties", char_vitality_propertie),
    h3_reflexive("placement_properties", char_placement_propertie),
    h3_reflexive("perception_properties", char_perception_propertie),
    h3_reflexive("look_properties", char_look_propertie),
    h3_reflexive("movement_properties", char_movement_propertie),
    h3_reflexive("unknown_0", char_unknown_0),
    h3_reflexive("swarm_properties", char_swarm_propertie),
    h3_reflexive("ready_properties", char_ready_propertie),
    h3_reflexive("engage_properties", char_engage_propertie),
    h3_reflexive("charge_properties", char_charge_propertie),
    h3_reflexive("evasion_properties", char_evasion_propertie),
    h3_reflexive("cover_properties", char_cover_propertie),
    h3_reflexive("retreat_properties", char_retreat_propertie),
    h3_reflexive("search_properties", char_search_propertie),
    h3_reflexive("pre_search_properties", char_pre_search_propertie),
    h3_reflexive("idle_properties", char_idle_propertie),
    h3_reflexive("vocalization_properties", char_vocalization_propertie),
    h3_reflexive("boarding_properties", char_boarding_propertie),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_2", char_unknown_2),
    h3_reflexive("unknown_3", char_unknown_3),
    h3_reflexive("weapons_properties", char_weapons_propertie),
    h3_reflexive("firing_pattern_properties", char_firing_pattern_propertie),
    h3_reflexive("grenades_properties", char_grenades_propertie),
    h3_reflexive("vehicle_properties", char_vehicle_propertie),
    h3_reflexive("morph_properties", char_morph_propertie),
    h3_reflexive("equipment_properties", char_equipment_propertie),
    h3_reflexive("metagame_properties", char_metagame_propertie),
    h3_reflexive("act_attachments", char_act_attachment),
    ENDIAN=">", SIZE=468
    )


def get():
    return char_def

char_def = TagDef("char",
    h3_blam_header('char'),
    char_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["char"], endian=">", tag_cls=H3Tag
    )
