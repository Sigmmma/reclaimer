#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
These are tags that halo custom edition will magically seek out at
runtime by their name. Not every map needs to have these, but depending
on which ones are missing, different things can happen.
Maps might not load, menus might not appear, sounds might not play, etc.
'''

# unicode_string_list
HARDCODED_ustr_TAG_PATHS = (
    "ui\\multiplayer_game_text.unicode_string_list",
    "ui\\random_player_names.unicode_string_list",

    "ui\\shell\\main_menu\\credits_screen.unicode_string_list",
    "ui\\shell\\main_menu\\map_list_short.unicode_string_list",
    "ui\\shell\\main_menu\\map_list_oneline.unicode_string_list",
    "ui\\shell\\main_menu\\mp_map_list.unicode_string_list",

    "ui\\shell\\main_menu\\multiplayer_type_select\\join_game\\join_game_rules_strings.unicode_string_list",
    "ui\\shell\\main_menu\\multiplayer_type_select\\join_game\\join_game_ticker_labels.unicode_string_list",

    "ui\\shell\\main_menu\\player_profiles_select\\button_set_long_descriptions.unicode_string_list",
    "ui\\shell\\main_menu\\player_profiles_select\\button_set_short_descriptions.unicode_string_list",# XBOX_ONLY
    "ui\\shell\\main_menu\\player_profiles_select\\joystick_set_defaults_descriptions.unicode_string_list",
    "ui\\shell\\main_menu\\player_profiles_select\\joystick_set_short_descriptions.unicode_string_list",
    "ui\\shell\\main_menu\\player_profiles_select\\profile_description_labels.unicode_string_list",

    "ui\\shell\\main_menu\\settings_select\\player_setup\\player_profile_edit\\color_edit\\colors_list.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\player_setup\\player_profile_edit\\controls_setup\\controls_axis_direction_names.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\player_setup\\player_profile_edit\\controls_setup\\controls_device_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\player_setup\\player_profile_edit\\controls_setup\\controls_gamepad_names.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\player_setup\\player_profile_edit\\controls_setup\\controls_keyboard_button_names.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\player_setup\\player_profile_edit\\controls_setup\\controls_mouse_button_names.unicode_string_list",

    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\item_options_edit\\var_weapon_set.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\player_options_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_invisible_players.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_maximum_health.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_number_of_lives.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_odd_man_out.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_respawn_time.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_respawn_time_growh.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_shields.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\player_options_edit\\var_suicide_penalty.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\ctf_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\var_assault.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\var_captures_to_win.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\var_flag_at_home.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\var_flag_must_reset.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\var_single_flag.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\ctf_edit\\var_time_limit.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\koth_edit\\koth_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\koth_edit\\var_moving_hill.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\koth_edit\\var_score_to_win.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\oddball_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\var_ball_spawn_count.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\var_ball_type.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\var_random_start.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\var_score_to_win.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\var_speed_with_ball.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\oddball_edit\\var_trait_with_ball.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\race_edit\\race_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\race_edit\\var_laps_to_win.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\race_edit\\var_race_type.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\race_edit\\var_team_play.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\race_edit\\var_team_scoring.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\slayer_edit\\slayer_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\slayer_edit\\var_death_bonus.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\slayer_edit\\var_kill_in_order.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\slayer_edit\\var_kill_penalty.unicode_string_list",# UNUSED?
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\slayer_edit\\var_kills_to_win.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\playlist_edit\\slayer_edit\\var_team_play.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\teamplay_options_edit\\teamplay_options_labels.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\teamplay_options_edit\\var_friendly_fire.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\teamplay_options_edit\\var_friendly_fire_penalty.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\vehicle_options_edit\\var_vehicle_set.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\vehicle_options_edit\\var_vehicles_respawn.unicode_string_list",
    "ui\\shell\\main_menu\\settings_select\\multiplayer_setup\\vehicle_options_edit\\vehicle_options_labels.unicode_string_list",

    "ui\\shell\\strings\\common_button_captions.unicode_string_list",
    "ui\\shell\\strings\\default_player_profile_names.unicode_string_list",
    "ui\\shell\\strings\\game_variant_descriptions.unicode_string_list",
    "ui\\shell\\strings\\loading.unicode_string_list",
    "ui\\shell\\strings\\temp_strings.unicode_string_list",
    )

# ui_widget_definition
HARDCODED_DeLa_TAG_PATHS = (
    "ui\\shell\\main_menu\\main_menu.ui_widget_definition",
    "ui\\shell\\main_menu\\multiplayer_type_select\\connected\\pregame\\connected_pregame_screen.ui_widget_definition",# XBOX_ONLY

    "ui\\shell\\multiplayer_game\\pause_game\\1p_pause_game.ui_widget_definition",
    "ui\\shell\\multiplayer_game\\pause_game\\2p_pause_game.ui_widget_definition",
    "ui\\shell\\multiplayer_game\\pause_game\\4p_pause_game.ui_widget_definition",

    "ui\\shell\\solo_game\\pause_game\\pause_game_split_screen.ui_widget_definition",
    "ui\\shell\\solo_game\\pause_game\\pause_game.ui_widget_definition",

    "ui\\shell\\solo_game\\player_help\\player_help_screen_a10.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_a30.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_a50.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_b30.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_b40.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_c10.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_c20.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_c40.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_d20.ui_widget_definition",
    "ui\\shell\\solo_game\\player_help\\player_help_screen_d40.ui_widget_definition",

    "ui\\shell\\error\\error_modal_fullscreen.ui_widget_definition",
    "ui\\shell\\error\\error_modal_halfscreen.ui_widget_definition",
    "ui\\shell\\error\\error_modal_qtrscreen.ui_widget_definition"
    "ui\\shell\\error\\error_nonmodal_fullscreen.ui_widget_definition",
    "ui\\shell\\error\\error_nonmodal_halfscreen.ui_widget_definition",
    "ui\\shell\\error\\error_nonmodal_qtrscreen.ui_widget_definition",
    )

# font
HARDCODED_font_TAG_PATHS = (
    "ui\\gamespy.font",
    "ui\\large_ui.font",
    "ui\\small_ui.font",
    )

# virtual_keyboard
HARDCODED_vcky_TAG_PATHS = (
    "ui\\english.virtual_keyboard",
    )

# bitmap
HARDCODED_bitm_TAG_PATHS = (
    "ui\\shell\\bitmaps\\cursor.bitmap",
    "ui\\shell\\bitmaps\\background.bitmap",
    "ui\\shell\\bitmaps\\team_background.bitmap",
    "ui\\shell\\bitmaps\\team_icon_slayer.bitmap",
    "ui\\shell\\bitmaps\\team_icon_race.bitmap",
    "ui\\shell\\bitmaps\\team_icon_oddball.bitmap",
    "ui\\shell\\bitmaps\\team_icon_king.bitmap",
    "ui\\shell\\bitmaps\\team_icon_ctf.bitmap",
    "ui\\shell\\bitmaps\\trouble_brewing.bitmap",
    "ui\\shell\\bitmaps\\white.bitmap",
    )


# globals
HARDCODED_matg_TAG_PATHS = (
    "globals\\globals.globals",
    )


# scenario
HARDCODED_scnr_TAG_PATHS = (
    "levels\\ui\\ui.scenario",
    )


# sound_looping
HARDCODED_lsnd_TAG_PATHS = (
    "sound\\music\\title1\\title1.sound_looping",
    )


# sound
HARDCODED_snd__TAG_PATHS = (
    "sound\\sfx\\ui\\flag_failure.sound",
    "sound\\sfx\\ui\\back.sound",
    "sound\\sfx\\ui\\forward.sound",
    "sound\\sfx\\ui\\cursor.sound",
    )

HARDCODED_TAG_PATHS = frozenset(
    HARDCODED_ustr_TAG_PATHS + HARDCODED_DeLa_TAG_PATHS +
    HARDCODED_font_TAG_PATHS + HARDCODED_vcky_TAG_PATHS +
    HARDCODED_bitm_TAG_PATHS +
    HARDCODED_matg_TAG_PATHS + HARDCODED_scnr_TAG_PATHS +
    HARDCODED_lsnd_TAG_PATHS + HARDCODED_snd__TAG_PATHS
    )
