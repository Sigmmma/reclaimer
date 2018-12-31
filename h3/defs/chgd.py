############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Namings and stuff
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

chgd_hud_global_biped = (
    "spartan",
    "elite",
    "monitor",
    )


chgd_hud_global_hud_attribute = Struct("hud_attribute", 
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
    QStruct("motion_sensor_offset", INCLUDE=xy_float),
    Float("motion_sensor_radius"),
    Float("motion_sensor_scale"),
    Float("horizontal_scale"),
    Float("vertical_scale"),
    Float("horizontal_stretch"),
    Float("vertical_stretch"),
    Float("notification_offset_y"),
    Float("state_left_right_offset_y"),
    Float("state_center_offset_y"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("state_scale"),
    Float("notification_scale"),
    Float("notification_line_spacing"),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    ENDIAN=">", SIZE=96
    )


chgd_hud_global_hud_sound = Struct("hud_sound", 
    h3_dependency("spartan_sound"),
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
    h3_dependency("elite_sound"),
    ENDIAN=">", SIZE=40
    )


chgd_hud_global_multiplayer_medal = Struct("multiplayer_medal", 
    h3_string_id("medal"),
    ENDIAN=">", SIZE=4
    )


chgd_hud_global = Struct("hud_global", 
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
    h3_reflexive("hud_attributes", chgd_hud_global_hud_attribute),
    h3_reflexive("hud_sounds", chgd_hud_global_hud_sound),
    h3_dependency("unknown_0"),
    h3_dependency("frag_grenade_swap_sound"),
    h3_dependency("plasma_grenade_swap_sound"),
    h3_dependency("spike_grenade_swap_sound"),
    h3_dependency("firebomb_grenade_swap_sound"),
    h3_dependency("damage_microtexture"),
    h3_dependency("damage_noise"),
    h3_dependency("directional_arrow"),
    h3_dependency("waypoints"),
    h3_dependency("scoreboard_hud"),
    h3_dependency("metagame_scoreboard_hud"),
    h3_dependency("theater_hud"),
    h3_dependency("forge_hud"),
    h3_dependency("hud_strings"),
    h3_dependency("medals"),
    h3_reflexive("multiplayer_medals", chgd_hud_global_multiplayer_medal),
    h3_dependency("medal_hud_animation"),
    h3_dependency("cortana_channel"),
    h3_dependency("unknown_1"),
    h3_dependency("unknown_2"),
    h3_dependency("jammer_response"),
    h3_dependency("jammer_shield_hit"),
    Float("grenade_scematics_spacing"),
    Float("equipment_scematic_offset_y"),
    Float("dual_equipment_scematic_offset_y"),
    Float("unknown_3", VISIBLE=False),
    Float("unknown_4", VISIBLE=False),
    Float("scoreboard_leader_offset_y"),
    BytesRaw("unknown_5", SIZE=4, VISIBLE=False),
    Float("waypoint_scale"),
    ENDIAN=">", SIZE=520
    )


chgd_hud_shader = Struct("hud_shader", 
    h3_dependency("vertex_shader"),
    h3_dependency("pixel_shader"),
    ENDIAN=">", SIZE=32
    )


chgd_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=64, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=64
    )


chgd_unknown_1_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=100, VISIBLE=False),
    h3_dependency("sound_0"),
    BytesRaw("unknown_1", SIZE=96, VISIBLE=False),
    h3_dependency("sound_1"),
    VISIBLE=False,
    ENDIAN=">", SIZE=228
    )


chgd_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", chgd_unknown_1_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


chgd_player_training_data = Struct("player_training_data", 
    h3_string_id("display_string"),
    SInt16("max_display_time"),
    SInt16("display_count"),
    SInt16("disappear_delay"),
    SInt16("redisplay_delay"),
    Float("display_delay"),
    Bool16("flags", 
        "not_in_multiplayer",
        ),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


chgd_body = Struct("tagdata", 
    h3_reflexive("hud_globals", chgd_hud_global),
    h3_reflexive("hud_shaders", chgd_hud_shader),
    h3_reflexive("unknown_0", chgd_unknown_0),
    h3_reflexive("unknown_1", chgd_unknown_1),
    h3_reflexive("player_training_data", chgd_player_training_data),
    h3_dependency("start_menu_emblems"),
    h3_dependency("campaign_medals"),
    h3_dependency("campaign_medal_hud_animation"),
    Float("campaign_medal_scale"),
    Float("campaign_medal_spacing"),
    QStruct("campaign_medal_offset", INCLUDE=xy_float),
    Float("metagame_scoreboard_top_y"),
    Float("metagame_scoreboard_spacing"),
    h3_dependency("unit_damage_grid"),
    Float("micro_texture_tile_amount"),
    Float("medium_sensor_blip_scale"),
    Float("small_sensor_blip_scale"),
    Float("large_sensor_blip_scale"),
    Float("sensor_blip_glow_amount"),
    Float("sensor_blip_glow_radius"),
    Float("sensor_blip_glow_opacity"),
    h3_dependency("motion_sensor_blip"),
    h3_dependency("birthday_party_effect"),
    h3_dependency("campaign_flood_mask"),
    h3_dependency("campaign_flood_mask_tile"),
    ENDIAN=">", SIZE=240
    )


def get():
    return chgd_def

chgd_def = TagDef("chgd",
    h3_blam_header('chgd'),
    chgd_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["chgd"], endian=">", tag_cls=H3Tag
    )
