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
# revision: 2		author: Deadcanadian
# 	naming whatever i can figure out
# revision: 3		author: Lord Zedd
# 	Yeah Buddy.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

wezr_capture_the_flag_variant_game_mode = (
    "multiple",
    "single",
    "neutral",
    )

wezr_capture_the_flag_variant_home_flag_waypoint = (
    "unknown_1",
    "unknown_2",
    "unknown_3",
    "not_in_single",
    )

wezr_capture_the_flag_variant_respawn_on_capture = (
    "disabled",
    "on_ally_capture",
    "on_enemy_capture",
    "on_any_capture",
    )

wezr_infection_variant_next_zombie = (
    "most_points",
    "first_infected",
    "unchanged",
    "random",
    )

wezr_infection_variant_safe_havens = (
    "none",
    "random",
    "sequence",
    )

wezr_juggernaut_variant_first_juggernaut = (
    "random",
    "first_kill",
    "first_death",
    )

wezr_juggernaut_variant_goal_zone_movement = (
    "no_movement",
    "after_10_seconds",
    "after_15_seconds",
    "after_30_seconds",
    "after_1_minute",
    "after_2_minutes",
    "after_3_minutes",
    "after_4_minutes",
    "after_5_minutes",
    "on_arrival",
    "on_new_juggernaut",
    )

wezr_juggernaut_variant_next_juggernaut = (
    "killer",
    "killed",
    "unchanged",
    "random",
    )

wezr_king_of_the_hill_variant_hill_movement = (
    "no_movement",
    "after_10_seconds",
    "after_15_seconds",
    "after_30_seconds",
    "after_1_minute",
    "after_2_minutes",
    "after_3_minutes",
    "after_4_minutes",
    "after_5_minutes",
    )

wezr_king_of_the_hill_variant_hill_movement_order = (
    "random",
    "sequence",
    )

wezr_king_of_the_hill_variant_team_scoring = (
    "sum",
    "minimum",
    "maximum",
    "default",
    )

wezr_sandbox_editor_variant_edit_mode = (
    "everyone",
    "leader_only",
    )

wezr_slayer_variant_general_setting_round_resets = (
    "nothing",
    "players_only",
    "everything",
    )

wezr_slayer_variant_team_scoring = (
    "sum_of_team",
    "minimum_score",
    "maximum_score",
    "default",
    )

wezr_trait_profile_appearance_active_camo = (
    "unchanged",
    "disabled",
    "bad_camo",
    "poor_camo",
    "good_camo",
    )

wezr_trait_profile_appearance_aura = (
    "unchanged",
    "disabled",
    "team",
    "black",
    "white",
    )

wezr_trait_profile_appearance_forced_color = (
    "unchanged",
    "off",
    "red",
    "blue",
    "green",
    "orange",
    "purple",
    "gold",
    "brown",
    "pink",
    "white",
    "black",
    "zombie",
    "pink_unused",
    )

wezr_trait_profile_appearance_waypoint = (
    "unchanged",
    "none",
    "visible_to_allies",
    "visible_to_everyone",
    )

wezr_trait_profile_movement_player_gravity = (
    "unchanged",
    "_50",
    "_75",
    "_100",
    "_150",
    "_200",
    )

wezr_trait_profile_movement_player_speed = (
    "unchanged",
    "_25",
    "_50",
    "_75",
    "_90",
    "_100",
    "_110",
    "_125",
    "_150",
    "_200",
    "_300",
    )

wezr_trait_profile_movement_vehicle_use = (
    "unchanged",
    "none",
    "passenger_only",
    "full_use",
    )

wezr_trait_profile_sensor_motion_tracker_mode = (
    "unchanged",
    "disabled",
    "ally_movement",
    "player_movement",
    "player_locations",
    )

wezr_trait_profile_sensor_motion_tracker_range = (
    "unchanged",
    "_10m",
    "_15m",
    "_25m",
    "_50m",
    "_75m",
    "_100m",
    "_150m",
    )

wezr_trait_profile_shields_and_health_damage_resistance = (
    "unchanged",
    "_10",
    "_50",
    "_90",
    "_100",
    "_110",
    "_150",
    "_200",
    "_300",
    "_500",
    "_1000",
    "_2000",
    "invulnerable",
    )

wezr_trait_profile_shields_and_health_headshot_immunity = (
    "unchanged",
    "enabled",
    "disabled",
    )

wezr_trait_profile_shields_and_health_shield_multiplier = (
    "unchanged",
    "no_shields",
    "normal_shields",
    "_2x_overshields",
    "_3x_overshields",
    "_4x_overshields",
    )

wezr_trait_profile_shields_and_health_shield_recharge_rate = (
    "unchanged",
    "neg_25",
    "neg_10",
    "neg_5",
    "_0",
    "_50",
    "_90",
    "_100",
    "_110",
    "_200",
    )

wezr_trait_profile_shields_and_health_shield_vampirism = (
    "unchanged",
    "disabled",
    "_10",
    "_25",
    "_50",
    "_100",
    )

wezr_trait_profile_weapons_and_damage_damage_modifier = (
    "unchanged",
    "_0",
    "_25",
    "_50",
    "_75",
    "_90",
    "_100",
    "_110",
    "_125",
    "_150",
    "_200",
    "_300",
    "instant_kill",
    )

wezr_trait_profile_weapons_and_damage_grenade_count = (
    "unchanged",
    "map_default",
    "none",
    )

wezr_trait_profile_weapons_and_damage_infinite_ammo = (
    "unchanged",
    "disabled",
    "enabled",
    )

wezr_vip_variant_goal_zone_movement = (
    "no_movement",
    "after_10_seconds",
    "after_15_seconds",
    "after_30_seconds",
    "after_1_minute",
    "after_2_minutes",
    "after_3_minutes",
    "after_4_minutes",
    "after_5_minutes",
    "on_arrival",
    "on_new_vip",
    )

wezr_vip_variant_next_vip = (
    "random",
    "unknown",
    "next_death",
    "unchanged",
    )


wezr_trait_profile_shields_and_health = Struct("shields_and_health",
    SEnum8("damage_resistance", *wezr_trait_profile_shields_and_health_damage_resistance),
    SEnum8("shield_multiplier", *wezr_trait_profile_shields_and_health_shield_multiplier),
    SEnum8("shield_recharge_rate", *wezr_trait_profile_shields_and_health_shield_recharge_rate),
    SEnum8("headshot_immunity", *wezr_trait_profile_shields_and_health_headshot_immunity),
    SEnum8("shield_vampirism", *wezr_trait_profile_shields_and_health_shield_vampirism),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


wezr_trait_profile_weapons_and_damage = Struct("weapons_and_damage",
    SEnum8("damage_modifier", *wezr_trait_profile_weapons_and_damage_damage_modifier),
    SEnum8("grenade_regeneration", *wezr_trait_profile_shields_and_health_headshot_immunity),
    SEnum8("weapon_pickup", *wezr_trait_profile_shields_and_health_headshot_immunity),
    SEnum8("infinite_ammo", *wezr_trait_profile_weapons_and_damage_infinite_ammo),
    h3_string_id("primary_weapon"),
    h3_string_id("secondary_weapon"),
    SEnum16("grenade_count", *wezr_trait_profile_weapons_and_damage_grenade_count),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_trait_profile_movement = Struct("movement",
    SEnum8("player_speed", *wezr_trait_profile_movement_player_speed),
    SEnum8("player_gravity", *wezr_trait_profile_movement_player_gravity),
    SEnum8("vehicle_use", *wezr_trait_profile_movement_vehicle_use),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


wezr_trait_profile_appearance = Struct("appearance",
    SEnum8("active_camo", *wezr_trait_profile_appearance_active_camo),
    SEnum8("waypoint", *wezr_trait_profile_appearance_waypoint),
    SEnum8("aura", *wezr_trait_profile_appearance_aura),
    SEnum8("forced_color", *wezr_trait_profile_appearance_forced_color),
    ENDIAN=">", SIZE=4
    )


wezr_trait_profile_sensor = Struct("sensor",
    SEnum32("motion_tracker_mode", *wezr_trait_profile_sensor_motion_tracker_mode),
    SEnum32("motion_tracker_range", *wezr_trait_profile_sensor_motion_tracker_range),
    ENDIAN=">", SIZE=8
    )


wezr_trait_profile = Struct("trait_profile",
    h3_string_id("name"),
    h3_reflexive("shields_and_health", wezr_trait_profile_shields_and_health),
    h3_reflexive("weapons_and_damage", wezr_trait_profile_weapons_and_damage),
    h3_reflexive("movement", wezr_trait_profile_movement),
    h3_reflexive("appearance", wezr_trait_profile_appearance),
    h3_reflexive("sensors", wezr_trait_profile_sensor),
    ENDIAN=">", SIZE=64
    )


wezr_slayer_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_slayer_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_slayer_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_slayer_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_slayer_variant = Struct("slayer_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_slayer_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_slayer_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_slayer_variant_social_setting),
    h3_reflexive("map_overrides", wezr_slayer_variant_map_override),
    SEnum16("team_scoring", *wezr_slayer_variant_team_scoring),
    SInt16("points_to_win"),
    SInt8("kill_points"),
    SInt8("assist_points"),
    SInt8("death_points"),
    SInt8("suicide_points"),
    SInt8("betrayal_points"),
    SInt8("leader_kill_bonus"),
    SInt8("elimination_bonus"),
    SInt8("assassination_bonus"),
    SInt8("headshot_bonus"),
    SInt8("beatdown_bonus"),
    SInt8("sticky_bonus"),
    SInt8("splatter_bonus"),
    SInt8("spree_bonus"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    h3_string_id("leader_trait_profile"),
    ENDIAN=">", SIZE=80
    )


wezr_oddball_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_oddball_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_oddball_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_oddball_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_oddball_variant = Struct("oddball_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_oddball_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_oddball_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_oddball_variant_social_setting),
    h3_reflexive("map_overrides", wezr_oddball_variant_map_override),
    Bool32("flags",
        "autopickup_enabled",
        "ball_effect_enabled",
        ),
    SEnum16("team_scoring", *wezr_slayer_variant_team_scoring),
    SInt16("points_to_win"),
    SInt8("carrying_points"),
    SInt8("kill_points"),
    SInt8("ball_kill_points"),
    SInt8("ball_carrier_kill_points"),
    SInt8("ball_count"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    SInt16("initial_ball_delay"),
    SInt16("ball_respawn_delay"),
    h3_string_id("ball_carrier_trait_profile"),
    ENDIAN=">", SIZE=80
    )


wezr_capture_the_flag_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_capture_the_flag_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_capture_the_flag_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_capture_the_flag_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_capture_the_flag_variant = Struct("capture_the_flag_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_capture_the_flag_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_capture_the_flag_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_capture_the_flag_variant_social_setting),
    h3_reflexive("map_overrides", wezr_capture_the_flag_variant_map_override),
    Bool32("flags",
        "flag_at_home_to_score",
        ),
    SEnum16("home_flag_waypoint", *wezr_capture_the_flag_variant_home_flag_waypoint),
    SEnum16("game_mode", *wezr_capture_the_flag_variant_game_mode),
    SEnum16("respawn_on_capture", *wezr_capture_the_flag_variant_respawn_on_capture),
    SInt16("flag_return_time"),
    SInt16("sudden_death_time"),
    SInt16("score_to_win"),
    SInt16("flag_reset_time"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    h3_string_id("flag_carrier_trait_profile"),
    ENDIAN=">", SIZE=80
    )


wezr_assault_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_assault_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_assault_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_assault_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_assault_variant = Struct("assault_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_assault_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_assault_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_assault_variant_social_setting),
    h3_reflexive("map_overrides", wezr_assault_variant_map_override),
    Bool32("flags",
        "reset_on_disarm",
        ),
    SEnum16("respawn_on_capture", *wezr_capture_the_flag_variant_respawn_on_capture),
    SEnum16("game_mode", *wezr_capture_the_flag_variant_game_mode),
    SEnum16("enemy_bomb_waypoint", *wezr_capture_the_flag_variant_home_flag_waypoint),
    SInt16("sudden_death_time"),
    SInt16("detonations_to_win"),
    SInt16("bomb_reset_time"),
    SInt16("bomb_arming_time"),
    SInt16("bomb_disarming_time"),
    SInt16("bomb_fuse_time"),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("bomb_carrier_trait_profile"),
    h3_string_id("unknown_trait_profile"),
    ENDIAN=">", SIZE=88
    )


wezr_infection_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_infection_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_infection_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_infection_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_infection_variant = Struct("infection_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_infection_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_infection_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_infection_variant_social_setting),
    h3_reflexive("map_overrides", wezr_infection_variant_map_override),
    Bool32("flags",
        "respawn_on_haven_move",
        ),
    SEnum16("safe_havens", *wezr_infection_variant_safe_havens),
    SEnum16("next_zombie", *wezr_infection_variant_next_zombie),
    SInt16("initial_zombie_count"),
    SInt16("safe_haven_movement_time"),
    SInt8("zombie_kill_points"),
    SInt8("infection_points"),
    SInt8("safe_haven_arrival_points"),
    SInt8("suicide_points"),
    SInt8("betrayal_points"),
    SInt8("last_man_standing_bonus"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    h3_string_id("zombie_trait_profile"),
    h3_string_id("alpha_zombie_trait_profile"),
    h3_string_id("on_haven_trait_profile"),
    h3_string_id("last_human_trait_profile"),
    ENDIAN=">", SIZE=92
    )


wezr_king_of_the_hill_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_king_of_the_hill_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_king_of_the_hill_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_king_of_the_hill_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_king_of_the_hill_variant = Struct("king_of_the_hill_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_king_of_the_hill_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_king_of_the_hill_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_king_of_the_hill_variant_social_setting),
    h3_reflexive("map_overrides", wezr_king_of_the_hill_variant_map_override),
    Bool32("flags",
        "opaque_hill",
        ),
    SInt16("score_to_win"),
    SEnum16("team_scoring", *wezr_king_of_the_hill_variant_team_scoring),
    SEnum16("hill_movement", *wezr_king_of_the_hill_variant_hill_movement),
    SEnum16("hill_movement_order", *wezr_king_of_the_hill_variant_hill_movement_order),
    SInt8("on_hill_points"),
    SInt8("uncontested_control_points"),
    SInt8("off_hill_points"),
    SInt8("kill_points"),
    h3_string_id("on_hill_trait_profile"),
    ENDIAN=">", SIZE=76
    )


wezr_territories_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_territories_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_territories_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_territories_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_territories_variant = Struct("territories_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_territories_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_territories_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_territories_variant_social_setting),
    h3_reflexive("map_overrides", wezr_territories_variant_map_override),
    Bool32("flags",
        "one_sided",
        "lock_after_first_capture",
        ),
    SEnum16("respawn_on_capture", *wezr_capture_the_flag_variant_respawn_on_capture),
    SInt16("territory_capture_time"),
    SInt16("sudden_death_time"),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("defender_trait_profile"),
    h3_string_id("attacker_trait_profile"),
    ENDIAN=">", SIZE=76
    )


wezr_juggernaut_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_juggernaut_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_juggernaut_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_juggernaut_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_juggernaut_variant = Struct("juggernaut_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_juggernaut_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_juggernaut_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_juggernaut_variant_social_setting),
    h3_reflexive("map_overrides", wezr_juggernaut_variant_map_override),
    Bool32("flags",
        "allied_against_juggernaut",
        "respawn_on_lone_juggernaut",
        "goal_zones_enabled",
        ),
    SEnum16("first_juggernaut", *wezr_juggernaut_variant_first_juggernaut),
    SEnum16("next_juggernaut", *wezr_juggernaut_variant_next_juggernaut),
    SEnum16("goal_zone_movement", *wezr_juggernaut_variant_goal_zone_movement),
    SEnum16("goal_zone_order", *wezr_king_of_the_hill_variant_hill_movement_order),
    SInt16("score_to_win"),
    SInt8("kill_points"),
    SInt8("takedown_points"),
    SInt8("kill_as_juggernaut_points"),
    SInt8("goal_arrival_points"),
    SInt8("suicide_points"),
    SInt8("betrayal_points"),
    SInt8("next_juggernaut_delay"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    h3_string_id("juggernaut_trait_profile"),
    ENDIAN=">", SIZE=84
    )


wezr_vip_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_vip_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_vip_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_vip_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_vip_variant = Struct("vip_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_vip_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_vip_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_vip_variant_social_setting),
    h3_reflexive("map_overrides", wezr_vip_variant_map_override),
    Bool32("flags",
        "single_vip",
        "goal_zones_enabled",
        "end_round_on_vip_death",
        ),
    SInt16("score_to_win"),
    SEnum16("next_vip", *wezr_vip_variant_next_vip),
    SEnum16("goal_zone_movement", *wezr_vip_variant_goal_zone_movement),
    SEnum16("goal_zone_movement_order", *wezr_king_of_the_hill_variant_hill_movement_order),
    SInt8("kill_points"),
    SInt8("vip_takedown_points"),
    SInt8("kill_as_vip_points"),
    SInt8("vip_death_points"),
    SInt8("goal_arrival_points"),
    SInt8("suicide_points"),
    SInt8("vip_betrayal_points"),
    SInt8("betrayal_points"),
    SInt8("vip_proximity_trait_radius"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    h3_string_id("vip_team_trait_profile"),
    h3_string_id("vip_proximity_trait_profile"),
    h3_string_id("vip_trait_profile"),
    ENDIAN=">", SIZE=92
    )


wezr_sandbox_editor_variant_general_setting = Struct("general_setting",
    Bool32("flags",
        "teams_enabled",
        ),
    SInt8("time_limit"),
    SInt8("number_of_rounds"),
    SInt8("early_victory_win_count"),
    SEnum8("round_resets", *wezr_slayer_variant_general_setting_round_resets),
    ENDIAN=">", SIZE=8
    )


wezr_sandbox_editor_variant_respawn_setting = Struct("respawn_setting",
    Bool16("flags",
        "inherit_respawn_time",
        "respawn_with_team",
        "respawn_at_location",
        "respawn_on_kills",
        ),
    SInt8("lives_per_round"),
    SInt8("shared_team_lives"),
    UInt8("respawn_time"),
    UInt8("suicide_penalty"),
    UInt8("betrayal_penalty"),
    UInt8("respawn_time_growth"),
    h3_string_id("respawn_trait_profile"),
    SInt8("respawn_trait_duration"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


wezr_sandbox_editor_variant_social_setting = Struct("social_setting",
    Bool32("flags",
        "observers_enabled",
        "team_changing_enabled",
        "balanced_team_changing",
        "friendly_fire_enabled",
        "betrayal_booting_enabled",
        "enemy_voice_enabled",
        "open_channel_voice_enabled",
        "dead_player_voice_enabled",
        ),
    ENDIAN=">", SIZE=4
    )


wezr_sandbox_editor_variant_map_override = Struct("map_override",
    Bool32("flags",
        "grenades_on_map",
        "indestructable_vehicles",
        ),
    h3_string_id("base_player_trait_profile"),
    h3_string_id("weapon_set"),
    h3_string_id("vehicle_set"),
    h3_string_id("overshield_trait_profile"),
    h3_string_id("active_camo_trait_profile"),
    h3_string_id("custom_powerup_trait_profile"),
    SInt8("overshield_trait_duration"),
    SInt8("active_camo_trait_duration"),
    SInt8("custom_powerup_trait_duration"),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


wezr_sandbox_editor_variant = Struct("sandbox_editor_variant",
    h3_string_id("name"),
    h3_string_id("description"),
    h3_reflexive("general_settings", wezr_sandbox_editor_variant_general_setting),
    h3_reflexive("respawn_settings", wezr_sandbox_editor_variant_respawn_setting),
    h3_reflexive("social_settings", wezr_sandbox_editor_variant_social_setting),
    h3_reflexive("map_overrides", wezr_sandbox_editor_variant_map_override),
    Bool32("flags",
        "open_channel_voice_enabled",
        ),
    SEnum16("edit_mode", *wezr_sandbox_editor_variant_edit_mode),
    SInt16("editor_respawn_time"),
    h3_string_id("editor_trait_profile"),
    ENDIAN=">", SIZE=68
    )


wezr_body = Struct("tagdata",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    h3_reflexive("trait_profiles", wezr_trait_profile),
    h3_reflexive("slayer_variants", wezr_slayer_variant),
    h3_reflexive("oddball_variants", wezr_oddball_variant),
    h3_reflexive("capture_the_flag_variants", wezr_capture_the_flag_variant),
    h3_reflexive("assault_variants", wezr_assault_variant),
    h3_reflexive("infection_variants", wezr_infection_variant),
    h3_reflexive("king_of_the_hill_variants", wezr_king_of_the_hill_variant),
    h3_reflexive("territories_variants", wezr_territories_variant),
    h3_reflexive("juggernaut_variants", wezr_juggernaut_variant),
    h3_reflexive("vip_variants", wezr_vip_variant),
    h3_reflexive("sandbox_editor_variants", wezr_sandbox_editor_variant),
    ENDIAN=">", SIZE=136
    )


def get():
    return wezr_def

wezr_def = TagDef("wezr",
    h3_blam_header('wezr'),
    wezr_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wezr"], endian=">", tag_cls=H3Tag
    )
