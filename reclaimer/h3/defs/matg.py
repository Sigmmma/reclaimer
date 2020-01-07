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
# revision: 2		author: shade45
# 	Named some values
# revision: 3		author: -DeToX-
# 	Named some reflexives and idents
# revision: 4		author: Veegie
# 	Mapped out reflextives and idents. Fixed titles.
# revision: 5		author: Lord Zedd
# 	Updates and standardizing
# revision: 6		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


matg_havok_cleanup_resource = Struct("havok_cleanup_resource",
    h3_dependency("object_cleanup_effect"),
    ENDIAN=">", SIZE=16
    )


matg_sound_global = Struct("sound_global",
    h3_dependency("sound_classes"),
    h3_dependency("sound_effects"),
    h3_dependency("sound_mix"),
    h3_dependency("sound_combat_dialogue_constants"),
    h3_dependency("sound_global_propagation"),
    ENDIAN=">", SIZE=80
    )


matg_ai_global_gravemind_propertie = QStruct("gravemind_propertie",
    Float("minimum_retreat_time"),
    Float("ideal_retreat_time"),
    Float("maximum_retreat_time"),
    ENDIAN=">", SIZE=12
    )


matg_ai_global_style = Struct("style",
    h3_dependency("style"),
    ENDIAN=">", SIZE=16
    )


matg_ai_global = Struct("ai_global",
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    Float("danger_broadly_facing"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    Float("danger_shooting_near"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    Float("danger_shooting_at"),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    Float("danger_extremely_close"),
    BytesRaw("unknown_4", SIZE=4, VISIBLE=False),
    Float("danger_shield_damage"),
    Float("danger_extended_shield_damage"),
    Float("danger_body_damage"),
    Float("danger_extended_body_damage"),
    BytesRaw("unknown_5", SIZE=48, VISIBLE=False),
    h3_dependency("global_dialogue"),
    h3_string_id("default_mission_dialogue_sound_effect"),
    BytesRaw("unknown_6", SIZE=20, VISIBLE=False),
    Float("jump_down"),
    Float("jump_step"),
    Float("jump_crouch"),
    Float("jump_stand"),
    Float("jump_storey"),
    Float("jump_tower"),
    Float("max_jump_down_height_down"),
    Float("max_jump_down_height_step"),
    Float("max_jump_down_height_crouch"),
    Float("max_jump_down_height_stand"),
    Float("max_jump_down_height_storey"),
    Float("max_jump_down_height_tower"),
    QStruct("hoist_step", INCLUDE=from_to),
    QStruct("hoist_crouch", INCLUDE=from_to),
    QStruct("hoist_stand", INCLUDE=from_to),
    BytesRaw("unknown_7", SIZE=24, VISIBLE=False),
    QStruct("vault_step", INCLUDE=from_to),
    QStruct("vault_crouch", INCLUDE=from_to),
    BytesRaw("unknown_8", SIZE=48, VISIBLE=False),
    h3_reflexive("gravemind_properties", matg_ai_global_gravemind_propertie),
    BytesRaw("unknown_9", SIZE=48, VISIBLE=False),
    Float("scary_target_threshold"),
    Float("scary_weapon_threshold"),
    BytesRaw("unknown_10", SIZE=44, VISIBLE=False),
    h3_reflexive("styles", matg_ai_global_style),
    ENDIAN=">", SIZE=432
    )


matg_damage_table_damage_group_armor_modifier = Struct("armor_modifier",
    h3_string_id("name"),
    Float("damage_multiplier"),
    ENDIAN=">", SIZE=8
    )


matg_damage_table_damage_group = Struct("damage_group",
    h3_string_id("name"),
    h3_reflexive("armor_modifiers", matg_damage_table_damage_group_armor_modifier),
    ENDIAN=">", SIZE=16
    )


matg_damage_table = Struct("damage_table",
    h3_reflexive("damage_groups", matg_damage_table_damage_group),
    ENDIAN=">", SIZE=12
    )


matg_sound = Struct("sound",
    h3_dependency("sound_obsolete"),
    ENDIAN=">", SIZE=16
    )


matg_camera = Struct("camera",
    h3_dependency("default_unit_camera_track"),
    Array("unknown_array_0", SUB_STRUCT=Float("unknown"), SIZE=24, VISIBLE=False),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=11, VISIBLE=False),
    ENDIAN=">", SIZE=160
    )


matg_player_control_look_function = QStruct("look_function",
    Float("scale"),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


matg_player_control = Struct("player_control",
    Float("magnetism_friction"),
    Float("magnetism_adhesion"),
    Float("inconsequential_target_scale"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    QStruct("crosshair_location", INCLUDE=xy_float),
    Float("seconds_to_start"),
    Float("seconds_to_full_speed"),
    Float("decay_rate"),
    Float("full_speed_multiplier"),
    Float("pegged_magnitude"),
    Float("pegged_angular_threshold"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    Float("look_default_pitch_rate"),
    Float("look_default_yaw_rate"),
    Float("look_peg_threshold"),
    Float("look_yaw_acceleration_time"),
    Float("look_yaw_acceleration_scale"),
    Float("look_pitch_acceleration_time"),
    Float("look_pitch_acceleration_scale"),
    Float("look_autoleveling_scale"),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    Float("gravity_scale"),
    SInt32("minimum_autoleveling_ticks"),
    float_rad("minimum_angle_for_vehicle_flipping"),
    h3_reflexive("look_function", matg_player_control_look_function),
    Float("minimum_action_hold_time"),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=136
    )


matg_difficulty = QStruct("difficulty",
    Float("easy_enemy_damage"),
    Float("normal_enemy_damage"),
    Float("hard_enemy_damage"),
    Float("impossible_enemy_damage"),
    Float("easy_enemy_vitality"),
    Float("normal_enemy_vitality"),
    Float("hard_enemy_vitality"),
    Float("impossible_enemy_vitality"),
    Float("easy_enemy_shield"),
    Float("normal_enemy_shield"),
    Float("hard_enemy_shield"),
    Float("impossible_enemy_shield"),
    Float("easy_enemy_recharge"),
    Float("normal_enemy_recharge"),
    Float("hard_enemy_recharge"),
    Float("impossible_enemy_recharge"),
    Float("easy_friend_damage"),
    Float("normal_friend_damage"),
    Float("hard_friend_damage"),
    Float("impossible_friend_damage"),
    Float("easy_friend_vitality"),
    Float("normal_friend_vitality"),
    Float("hard_friend_vitality"),
    Float("impossible_friend_vitality"),
    Float("easy_friend_shield"),
    Float("normal_friend_shield"),
    Float("hard_friend_shield"),
    Float("impossible_friend_shield"),
    Float("easy_friend_recharge"),
    Float("normal_friend_recharge"),
    Float("hard_friend_recharge"),
    Float("impossible_friend_recharge"),
    Float("easy_infection_forms"),
    Float("normal_infection_forms"),
    Float("hard_infection_forms"),
    Float("impossible_infection_forms"),
    Float("easy_unknown_0", VISIBLE=False),
    Float("normal_unknown_0", VISIBLE=False),
    Float("hard_unknown_0", VISIBLE=False),
    Float("impossible_unknown_0", VISIBLE=False),
    Float("easy_rate_of_fire"),
    Float("normal_rate_of_fire"),
    Float("hard_rate_of_fire"),
    Float("impossible_rate_of_fire"),
    Float("easy_projectile_error"),
    Float("normal_projectile_error"),
    Float("hard_projectile_error"),
    Float("impossible_projectile_error"),
    Float("easy_burst_error"),
    Float("normal_burst_error"),
    Float("hard_burst_error"),
    Float("impossible_burst_error"),
    Float("easy_target_delay"),
    Float("normal_target_delay"),
    Float("hard_target_delay"),
    Float("impossible_target_delay"),
    Float("easy_burst_separation"),
    Float("normal_burst_separation"),
    Float("hard_burst_separation"),
    Float("impossible_burst_separation"),
    Float("easy_target_tracking"),
    Float("normal_target_tracking"),
    Float("hard_target_tracking"),
    Float("impossible_target_tracking"),
    Float("easy_target_leading"),
    Float("normal_target_leading"),
    Float("hard_target_leading"),
    Float("impossible_target_leading"),
    Float("easy_overcharge_chance"),
    Float("normal_overcharge_chance"),
    Float("hard_overcharge_chance"),
    Float("impossible_overcharge_chance"),
    Float("easy_special_fire_delay"),
    Float("normal_special_fire_delay"),
    Float("hard_special_fire_delay"),
    Float("impossible_special_fire_delay"),
    Float("easy_guidance_vs_player"),
    Float("normal_guidance_vs_player"),
    Float("hard_guidance_vs_player"),
    Float("impossible_guidance_vs_player"),
    Float("easy_melee_delay_base"),
    Float("normal_melee_delay_base"),
    Float("hard_melee_delay_base"),
    Float("impossible_melee_delay_base"),
    Float("easy_melee_delay_scale"),
    Float("normal_melee_delay_scale"),
    Float("hard_melee_delay_scale"),
    Float("impossible_melee_delay_scale"),
    Float("easy_unknown_1", VISIBLE=False),
    Float("normal_unknown_1", VISIBLE=False),
    Float("hard_unknown_1", VISIBLE=False),
    Float("impossible_unknown_1", VISIBLE=False),
    Float("easy_grenade_chance_scale"),
    Float("normal_grenade_chance_scale"),
    Float("hard_grenade_chance_scale"),
    Float("impossible_grenade_chance_scale"),
    Float("easy_grenade_timer_scale"),
    Float("normal_grenade_timer_scale"),
    Float("hard_grenade_timer_scale"),
    Float("impossible_grenade_timer_scale"),
    Float("easy_unknown_2", VISIBLE=False),
    Float("normal_unknown_2", VISIBLE=False),
    Float("hard_unknown_2", VISIBLE=False),
    Float("impossible_unknown_2", VISIBLE=False),
    Float("easy_unknown_3", VISIBLE=False),
    Float("normal_unknown_3", VISIBLE=False),
    Float("hard_unknown_3", VISIBLE=False),
    Float("impossible_unknown_3", VISIBLE=False),
    Float("easy_unknown_4", VISIBLE=False),
    Float("normal_unknown_4", VISIBLE=False),
    Float("hard_unknown_4", VISIBLE=False),
    Float("impossible_unknown_4", VISIBLE=False),
    Float("easy_major_upgrade_normal"),
    Float("normal_major_upgrade_normal"),
    Float("hard_major_upgrade_normal"),
    Float("impossible_major_upgrade_normal"),
    Float("easy_major_upgrade_few"),
    Float("normal_major_upgrade_few"),
    Float("hard_major_upgrade_few"),
    Float("impossible_major_upgrade_few"),
    Float("easy_major_upgrade_many"),
    Float("normal_major_upgrade_many"),
    Float("hard_major_upgrade_many"),
    Float("impossible_major_upgrade_many"),
    Float("easy_player_vehicle_ram_chance"),
    Float("normal_player_vehicle_ram_chance"),
    Float("hard_player_vehicle_ram_chance"),
    Float("impossible_player_vehicle_ram_chance"),
    Pad(132),
    ENDIAN=">", SIZE=644
    )


matg_grenade = Struct("grenade",
    SInt16("maximum_count"),
    SInt16("unknown_0", VISIBLE=False),
    h3_dependency("throwing_effect"),
    BytesRaw("unknown_1", SIZE=16, VISIBLE=False),
    h3_dependency("equipment"),
    h3_dependency("projectile"),
    ENDIAN=">", SIZE=68
    )


matg_interface_tag = Struct("interface_tag",
    h3_dependency("spinner"),
    h3_dependency("obsolete"),
    h3_dependency("screen_color_table"),
    h3_dependency("hud_color_table"),
    h3_dependency("editor_color_table"),
    h3_dependency("dialog_color_table"),
    h3_dependency("motion_sensor_sweep_bitmap"),
    h3_dependency("motion_sensor_sweep_bitmap_mask"),
    h3_dependency("multiplayer_hud_bitmap"),
    h3_dependency("hud_digits_definition"),
    h3_dependency("motion_sensor_blip_bitmap"),
    h3_dependency("interface_goo_map_1"),
    h3_dependency("interface_goo_map_2"),
    h3_dependency("interface_goo_map_3"),
    h3_dependency("main_menu_ui_globals"),
    h3_dependency("single_player_ui_globals"),
    h3_dependency("multiplayer_ui_globals"),
    h3_dependency("hud_globals"),
    ENDIAN=">", SIZE=288
    )


matg_player_information = Struct("player_information",
    Float("walking_speed"),
    Float("run_forward"),
    Float("run_backward"),
    Float("run_sideways"),
    Float("run_acceleration", VISIBLE=False),
    Float("sneak_forward"),
    Float("sneak_backward"),
    Float("sneak_sideways"),
    Float("sneak_acceleration"),
    Float("airborne_acceleration"),
    QStruct("grenade_origin", INCLUDE=xyz_float),
    Float("stun_movement_penalty"),
    Float("stun_turning_penalty"),
    Float("stun_jumping_penalty"),
    QStruct("stun_time", INCLUDE=from_to),
    QStruct("first_person_idle_time", INCLUDE=from_to),
    Float("first_person_skip_fraction"),
    h3_dependency("unknown_0", VISIBLE=False),
    h3_dependency("unknown_1", VISIBLE=False),
    h3_dependency("coop_respawn_effect"),
    SInt32("binoculars_zoom_count"),
    QStruct("binocular_zoom_range", INCLUDE=from_to),
    h3_dependency("flashlight_on"),
    h3_dependency("flashlight_off"),
    h3_dependency("default_damage_response"),
    ENDIAN=">", SIZE=192
    )


matg_player_representation = Struct("player_representation",
    h3_dependency("first_person_hands"),
    h3_dependency("first_person_body"),
    h3_dependency("third_person_unit"),
    h3_string_id("third_person_variant"),
    h3_dependency("binoculars_zoom_in_sound"),
    h3_dependency("binoculars_zoom_out_sound"),
    ENDIAN=">", SIZE=84
    )


matg_falling_damage = Struct("falling_damage",
    QStruct("harmful_falling_distance", INCLUDE=from_to),
    h3_dependency("falling_damage"),
    h3_dependency("unknown_0", VISIBLE=False),
    h3_dependency("soft_landing"),
    h3_dependency("hard_landing"),
    h3_dependency("script_damage"),
    Float("maximum_falling_distance"),
    h3_dependency("distance_damage"),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=120
    )


matg_material_water_drag_propertie = Struct("water_drag_propertie",
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=9),
    Pad(4),
    VISIBLE=False,
    ENDIAN=">", SIZE=40
    )


matg_material_water_interaction = Struct("water_interaction",
    h3_string_id("surface_name"),
    h3_string_id("submerged_name"),
    SInt16("surface_index"),
    SInt16("submerged_index"),
    ENDIAN=">", SIZE=12
    )


matg_material = Struct("material",
    h3_string_id("name"),
    h3_string_id("parent_name"),
    SInt16("parent_index"),
    Bool16("flags", *unknown_flags_16),
    h3_string_id("general_armor"),
    h3_string_id("specific_armor"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    Float("friction"),
    Float("restitution"),
    Float("density"),
    h3_reflexive("water_drag_properties", matg_material_water_drag_propertie),
    h3_dependency("breakable_surface"),
    h3_dependency("sound_sweetener_small"),
    h3_dependency("sound_sweetener_medium"),
    h3_dependency("sound_sweetener_large"),
    h3_dependency("sound_sweetener_rolling"),
    h3_dependency("sound_sweetener_grinding"),
    h3_dependency("sound_sweetener_melee_small"),
    h3_dependency("sound_sweetener_melee_medium"),
    h3_dependency("sound_sweetener_melee_large"),
    h3_dependency("effect_sweetener_small"),
    h3_dependency("effect_sweetener_medium"),
    h3_dependency("effect_sweetener_large"),
    h3_dependency("effect_sweetener_rolling"),
    h3_dependency("effect_sweetener_grinding"),
    h3_dependency("effect_sweetener_melee"),
    h3_dependency("water_ripple_small"),
    h3_dependency("water_ripple_medium"),
    h3_dependency("water_ripple_large"),
    Bool32("sweetener_inheritance_flags",
        "sound_small",
        "sound_medium",
        "sound_large",
        "sound_rolling",
        "sound_grinding",
        "sound_melee_small",
        "sound_melee_medium",
        "sound_melee_large",
        "effect_small",
        "effect_medium",
        "effect_large",
        "effect_rolling",
        "effect_grinding",
        "effect_melee",
        "water_ripple_small",
        "water_ripple_medium",
        "water_ripple_large",
        ),
    h3_dependency("material_effects"),
    h3_reflexive("water_interaction", matg_material_water_interaction),
    ENDIAN=">", SIZE=368
    )


matg_player_color = Struct("player_color",
    color_rgb_float("color"),
    ENDIAN=">", SIZE=12
    )


matg_cinematic_anchor = Struct("cinematic_anchor",
    h3_dependency("cinematic_anchor"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


matg_metagame_global_medal = QStruct("medal",
    Float("multiplier"),
    ENDIAN=">", SIZE=4
    )


matg_metagame_global_difficulty = QStruct("difficulty",
    Float("multiplier"),
    ENDIAN=">", SIZE=4
    )


matg_metagame_global_primary_skull = QStruct("primary_skull",
    Float("multiplier"),
    ENDIAN=">", SIZE=4
    )


matg_metagame_global_secondary_skull = QStruct("secondary_skull",
    Float("multiplier"),
    ENDIAN=">", SIZE=4
    )


matg_metagame_global = Struct("metagame_global",
    h3_reflexive("medals", matg_metagame_global_medal),
    h3_reflexive("difficulty", matg_metagame_global_difficulty),
    h3_reflexive("primary_skulls", matg_metagame_global_primary_skull),
    h3_reflexive("secondary_skulls", matg_metagame_global_secondary_skull),
    SInt32("unknown_0"),
    SInt32("death_penalty"),
    SInt32("betrayal_penalty"),
    SInt32("unknown_1", VISIBLE=False),
    Float("multikill_window"),
    Float("emp_window"),
    ENDIAN=">", SIZE=72
    )


matg_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=172, VISIBLE=False),
    SEnum32("language", *ugh__language_language),
    h3_reflexive("havok_cleanup_resources", matg_havok_cleanup_resource),
    h3_reflexive("sound_globals", matg_sound_global),
    h3_reflexive("ai_globals", matg_ai_global),
    h3_reflexive("damage_table", matg_damage_table),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    h3_reflexive("sounds", matg_sound),
    h3_reflexive("camera", matg_camera),
    h3_reflexive("player_control", matg_player_control),
    h3_reflexive("difficulty", matg_difficulty),
    h3_reflexive("grenades", matg_grenade),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    h3_reflexive("interface_tags", matg_interface_tag),
    BytesRaw("unknown_3", SIZE=24, VISIBLE=False),
    h3_reflexive("player_information", matg_player_information),
    h3_reflexive("player_representation", matg_player_representation),
    h3_reflexive("falling_damage", matg_falling_damage),
    h3_reflexive("materials", matg_material),
    h3_reflexive("player_colors", matg_player_color),
    h3_dependency("multiplayer_globals"),
    h3_reflexive("cinematic_anchors", matg_cinematic_anchor),
    h3_reflexive("metagame_globals", matg_metagame_global),
    UInt32("unknown_4", VISIBLE=False),
    UInt32("unknown_5", VISIBLE=False),
    UInt32("string_count_0"),
    UInt32("locale_table_size_0"),
    UInt32("locale_index_table_offset_0"),
    UInt32("locale_data_index_offset_0"),
    BytesRaw("index_table_hash_0", SIZE=20),
    BytesRaw("string_data_hash_0", SIZE=20),
    UInt32("unknown_6", VISIBLE=False),
    UInt32("unknown_7", VISIBLE=False),
    UInt32("unknown_8", VISIBLE=False),
    UInt32("string_count_1"),
    UInt32("locale_table_size_1"),
    UInt32("locale_index_table_offset_1"),
    UInt32("locale_data_index_offset_1"),
    BytesRaw("index_table_hash_1", SIZE=20),
    BytesRaw("string_data_hash_1", SIZE=20),
    UInt32("unknown_9", VISIBLE=False),
    UInt32("unknown_10", VISIBLE=False),
    UInt32("unknown_11", VISIBLE=False),
    UInt32("string_count_2"),
    UInt32("locale_table_size_2"),
    UInt32("locale_index_table_offset_2"),
    UInt32("locale_data_index_offset_2"),
    BytesRaw("index_table_hash_2", SIZE=20),
    BytesRaw("string_data_hash_2", SIZE=20),
    UInt32("unknown_12", VISIBLE=False),
    UInt32("unknown_13", VISIBLE=False),
    UInt32("unknown_14", VISIBLE=False),
    UInt32("string_count_3"),
    UInt32("locale_table_size_3"),
    UInt32("locale_index_table_offset_3"),
    UInt32("locale_data_index_offset_3"),
    BytesRaw("index_table_hash_3", SIZE=20),
    BytesRaw("string_data_hash_3", SIZE=20),
    UInt32("unknown_15", VISIBLE=False),
    UInt32("unknown_16", VISIBLE=False),
    UInt32("unknown_17", VISIBLE=False),
    UInt32("string_count_4"),
    UInt32("locale_table_size_4"),
    UInt32("locale_index_table_offset_4"),
    UInt32("locale_data_index_offset_4"),
    BytesRaw("index_table_hash_4", SIZE=20),
    BytesRaw("string_data_hash_4", SIZE=20),
    UInt32("unknown_18", VISIBLE=False),
    UInt32("unknown_19", VISIBLE=False),
    UInt32("unknown_20", VISIBLE=False),
    UInt32("string_count_5"),
    UInt32("locale_table_size_5"),
    UInt32("locale_index_table_offset_5"),
    UInt32("locale_data_index_offset_5"),
    BytesRaw("index_table_hash_5", SIZE=20),
    BytesRaw("string_data_hash_5", SIZE=20),
    UInt32("unknown_21", VISIBLE=False),
    UInt32("unknown_22", VISIBLE=False),
    UInt32("unknown_23", VISIBLE=False),
    UInt32("string_count_6"),
    UInt32("locale_table_size_6"),
    UInt32("locale_index_table_offset_6"),
    UInt32("locale_data_index_offset_6"),
    BytesRaw("index_table_hash_6", SIZE=20),
    BytesRaw("string_data_hash_6", SIZE=20),
    UInt32("unknown_24", VISIBLE=False),
    UInt32("unknown_25", VISIBLE=False),
    UInt32("unknown_26", VISIBLE=False),
    UInt32("string_count_7"),
    UInt32("locale_table_size_7"),
    UInt32("locale_index_table_offset_7"),
    UInt32("locale_data_index_offset_7"),
    BytesRaw("index_table_hash_7", SIZE=20),
    BytesRaw("string_data_hash_7", SIZE=20),
    UInt32("unknown_27", VISIBLE=False),
    UInt32("unknown_28", VISIBLE=False),
    UInt32("unknown_29", VISIBLE=False),
    UInt32("string_count_8"),
    UInt32("locale_table_size_8"),
    UInt32("locale_index_table_offset_8"),
    UInt32("locale_data_index_offset_8"),
    BytesRaw("index_table_hash_8", SIZE=20),
    BytesRaw("string_data_hash_8", SIZE=20),
    UInt32("unknown_30", VISIBLE=False),
    UInt32("unknown_31", VISIBLE=False),
    UInt32("unknown_32", VISIBLE=False),
    UInt32("string_count_9"),
    UInt32("locale_table_size_9"),
    UInt32("locale_index_table_offset_9"),
    UInt32("locale_data_index_offset_9"),
    BytesRaw("index_table_hash_9", SIZE=20),
    BytesRaw("string_data_hash_9", SIZE=20),
    UInt32("unknown_33", VISIBLE=False),
    UInt32("unknown_34", VISIBLE=False),
    UInt32("unknown_35", VISIBLE=False),
    UInt32("string_count_10"),
    UInt32("locale_table_size_10"),
    UInt32("locale_index_table_offset_10"),
    UInt32("locale_data_index_offset_10"),
    BytesRaw("index_table_hash_10", SIZE=20),
    BytesRaw("string_data_hash_10", SIZE=20),
    UInt32("unknown_36", VISIBLE=False),
    UInt32("unknown_37", VISIBLE=False),
    UInt32("unknown_38", VISIBLE=False),
    UInt32("string_count_11"),
    UInt32("locale_table_size_11"),
    UInt32("locale_index_table_offset_11"),
    UInt32("locale_data_index_offset_11"),
    BytesRaw("index_table_hash_11", SIZE=20),
    BytesRaw("string_data_hash_11", SIZE=20),
    UInt32("unknown_39", VISIBLE=False),
    h3_dependency("rasterizer_globals"),
    h3_dependency("default_camera_effect"),
    h3_dependency("default_wind"),
    h3_dependency("default_damage_effect"),
    h3_dependency("default_collision_damage"),
    h3_string_id("unknown_material"),
    SInt16("unknown_global_material_index"),
    SInt16("unknown_40", VISIBLE=False),
    h3_dependency("effect_globals"),
    BytesRaw("unknown_41", SIZE=172, VISIBLE=False),
    ENDIAN=">", SIZE=1536
    )


def get():
    return matg_def

matg_def = TagDef("matg",
    h3_blam_header('matg'),
    matg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["matg"], endian=">", tag_cls=H3Tag
    )
