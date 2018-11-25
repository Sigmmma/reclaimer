from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

chgd_hud_global_biped = (
    "spartan",
    "elite",
    "monitor",
    )


chgd_hud_global_hud_attribute = Struct("hud_attributes",
    Bool32("resolution_flags",
        "wide_full",
        "wide_half",
        ("standard_full", 1 << 3),
        "wide_quarter",
        "standard_half",
        ("standard_quarter", 1 << 7),
        ),
    float_rad("warp_angle"),
    Float("warp_amount"),
    Float("warp_direction"),
    UInt32("resolution_width"),
    UInt32("resolution_height"),
    Float("motion_sensor_offset_x"),
    Float("motion_sensor_offset_y"),
    Float("motion_sensor_radius"),
    Float("motion_sensor_scale"),
    Float("horizontal_scale"),
    Float("vertical_scale"),
    Float("horizontal_stretch"),
    Float("vertical_stretch"),
    Float("notification_offset_y"),
    Float("state_left_right_offset_y"),
    Float("state_center_offset_y"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("state_scale"),
    Float("notification_scale"),
    Float("notification_line_spacing"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=96
    )


chgd_hud_global_hud_sound = Struct("hud_sounds",
    dependency("spartan_sound"),
    Bool32("latched_to",
        "shield_recharging",
        "shield_damaged",
        "shield_low",
        "shield_empty",
        "health_low",
        "health_empty",
        "health_minor_damage",
        "health_major_damage",
        "rocket_locking",
        "rocket_locked",
        "missile_locking",
        "missile_locked",
        ),
    Float("scale"),
    dependency("elite_sound"),
    ENDIAN=">", SIZE=40
    )


chgd_hud_global_multiplayer_medal = Struct("multiplayer_medals",
    string_id_meta("medal"),
    ENDIAN=">", SIZE=4
    )


chgd_hud_global = Struct("hud_globals",
    SEnum32("biped", *chgd_hud_global_biped),
    color_argb_uint32("_0_hud_disabled"),
    color_argb_uint32("_1_hud_primary"),
    color_argb_uint32("_2_hud_foreground"),
    color_argb_uint32("_3_hud_warning"),
    color_argb_uint32("_4_neutral_reticule"),
    color_argb_uint32("_5_hostile_reticule"),
    color_argb_uint32("_6_friendly_reticule"),
    color_argb_uint32("_7"),
    color_argb_uint32("_8_neutral_blip"),
    color_argb_uint32("_9_hostile_blip"),
    color_argb_uint32("_10_friendly_player_blip"),
    color_argb_uint32("_11_friendly_ai_blip"),
    color_argb_uint32("_12"),
    color_argb_uint32("_13_waypoint_blip"),
    color_argb_uint32("_14_distant_waypoint_blip"),
    color_argb_uint32("_15_waypoint"),
    color_argb_uint32("_16"),
    color_argb_uint32("_17"),
    color_argb_uint32("_18"),
    color_argb_uint32("_19"),
    color_argb_uint32("_20"),
    color_argb_uint32("_21"),
    color_argb_uint32("_22_text_fade_in"),
    color_argb_uint32("_23"),
    color_argb_uint32("_24"),
    color_argb_uint32("_25"),
    color_argb_uint32("_26"),
    color_argb_uint32("_27"),
    reflexive("hud_attributes", chgd_hud_global_hud_attribute),
    reflexive("hud_sounds", chgd_hud_global_hud_sound),
    dependency("unknown"),
    dependency("frag_grenade_swap_sound"),
    dependency("plasma_grenade_swap_sound"),
    dependency("spike_grenade_swap_sound"),
    dependency("firebomb_grenade_swap_sound"),
    dependency("damage_microtexture"),
    dependency("damage_noise"),
    dependency("directional_arrow"),
    dependency("waypoints"),
    dependency("scoreboard_hud"),
    dependency("metagame_scoreboard_hud"),
    dependency("theater_hud"),
    dependency("forge_hud"),
    dependency("hud_strings"),
    dependency("medals"),
    reflexive("multiplayer_medals", chgd_hud_global_multiplayer_medal),
    dependency("medal_hud_animation"),
    dependency("cortana_channel"),
    dependency("unknown_1"),
    dependency("unknown_2"),
    dependency("jammer_response"),
    dependency("jammer_shield_hit"),
    Float("grenade_scematics_spacing"),
    Float("equipment_scematic_offset_y"),
    Float("dual_equipment_scematic_offset_y"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("scoreboard_leader_offset_y"),
    Pad(4),
    Float("waypoint_scale"),
    ENDIAN=">", SIZE=520
    )


chgd_hud_shader = Struct("hud_shaders",
    dependency("vertex_shader"),
    dependency("pixel_shader"),
    ENDIAN=">", SIZE=32
    )


chgd_unknown = Struct("unknown",
    Pad(64),
    ENDIAN=">", SIZE=64
    )


chgd_unknown_1_unknown_1 = Struct("unknown_1",
    Pad(100),
    dependency("sound"),
    Pad(96),
    dependency("sound_1"),
    ENDIAN=">", SIZE=228
    )


chgd_unknown_1 = Struct("unknown_1",
    Pad(4),
    reflexive("unknown_1", chgd_unknown_1_unknown_1),
    ENDIAN=">", SIZE=16
    )


chgd_player_training_data = Struct("player_training_data",
    string_id_meta("display_string"),
    SInt16("max_display_time"),
    SInt16("display_count"),
    SInt16("disappear_delay"),
    SInt16("redisplay_delay"),
    Float("display_delay"),
    Bool16("flags",
        "not_in_multiplayer",
        ),
    SInt16("unknown"),
    ENDIAN=">", SIZE=20
    )


chgd_meta_def = BlockDef("chgd",
    reflexive("hud_globals", chgd_hud_global),
    reflexive("hud_shaders", chgd_hud_shader),
    reflexive("unknown", chgd_unknown),
    reflexive("unknown_1", chgd_unknown_1),
    reflexive("player_training_data", chgd_player_training_data),
    dependency("start_menu_emblems"),
    dependency("campaign_medals"),
    dependency("campaign_medal_hud_animation"),
    Float("campaign_medal_scale"),
    Float("campaign_medal_spacing"),
    Float("campaign_medal_offset_x"),
    Float("campaign_medal_offset_y"),
    Float("metagame_scoreboard_top_y"),
    Float("metagame_scoreboard_spacing"),
    dependency("unit_damage_grid"),
    Float("micro_texture_tile_amount"),
    Float("medium_sensor_blip_scale"),
    Float("small_sensor_blip_scale"),
    Float("large_sensor_blip_scale"),
    Float("sensor_blip_glow_amount"),
    Float("sensor_blip_glow_radius"),
    Float("sensor_blip_glow_opacity"),
    dependency("motion_sensor_blip"),
    dependency("birthday_party_effect"),
    dependency("campaign_flood_mask"),
    dependency("campaign_flood_mask_tile"),
    TYPE=Struct, ENDIAN=">", SIZE=240
    )