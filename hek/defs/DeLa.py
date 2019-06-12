from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# Typing these up took FOREVER
game_data_input_functions = (
    'NULL', 'player_settings_menu_update', 'unused',
    'playlist_settings_menu_update', 'gametype_select_menu_update',
    'multiplayer_type_menu_update', 'solo_level_select_update',
    'difficulty_menu_update', 'build_number',  # textbox only for build_number
    'server_list_update', 'network_pregame_status_update',
    'splitscreen_pregame_update', 'net_splitscreen_prejoin_players',
    'mp_profile_list_update', 'wide_3_player_profile_list_update',
    'player_profile_edit_select_menu_update',
    'player_profile_small_menu_update', 'game_settings_lists_text_update',
    'solo_game_objective_text', 'color_picker_update',
    'game_setings_lists_pic_update', 'main_menu_fake_animate',
    'mp_level_select_update',
    'get_active_player_profile_name', 'get_edit_player_profile_name',
    'get_edit_game_settings_name', 'get_active_player_profile_color',
    'mp_set_textbox_map_name', 'mp_set_textbox_game_rules',
    'mp_set_textbox_teams_no_teams', 'mp_set_textbox_score_limit',
    'mp_set_textbox_score_limit_type', 'mp_set_bitmap_for_map',
    'mp_set_bitmap_for_ruleset', 'mp_set_textbox_player_count',
    'mp_edit_profile_set_rule_text',
    'system_link_status_check', 'mp_game_directions',
    'teams_no_teams_bitmap_update', 'warn_if_diff_will_nuke_saved_game',
    'dim_if_no_net_cable', 'pause_game_set_textbox_inverted',
    'dim_unless_two_controllers', 'controls_update_menu',
    'video_menu_update', 'gamespy_screen_update', 'common_button_bar_update',
    'gamepad_update_menu', 'server_settings_update', 'audio_menu_update',
    'mp_profile_vehicles_update', 'solo_map_list_update', 'mp_map_list_update',
    'gametype_select_list_update', 'gametype_edit_list_update',
    'load_game_list_update', 'checking_for_updates',
    'direct_ip_connect_update', 'network_settings_update',
    )
event_types = (
    'A_button', 'B_button', 'X_button', 'Y_button',
    'black_button', 'white_button', 'left_trigger', 'right_trigger',
    'dpad_up', 'dpad_down', 'dpad_left', 'dpad_right',
    'start_button', 'back_button', 'left_thumb', 'right_thumb',
    'left_analog_stick_up', 'left_analog_stick_down',
    'left_analog_stick_left', 'left_analog_stick_right',
    'right_analog_stick_up', 'right_analog_stick_down',
    'right_analog_stick_left', 'right_analog_stick_right',
    'created', 'deleted', 'get_focus', 'lose_focus',
    'left_mouse', 'middle_mouse', 'right_mouse', 'double_click',
    'custom_activation', 'post_render'
    )
event_functions = (
    'NULL', 'list_goto_next_item', 'list_goto_previous_item',
    'unused1', 'unused2', 'initialize_sp_level_list_solo',
    'initialize_sp_level_list_coop', 'dispose_sp_level_list',
    'solo_level_set_map', 'set_difficulty', 'start_new_game',
    'pause_game_restart_at_checkpoint', 'pause_game_restart_level',
    'pause_game_rturn_to_main_menu', 'clear_multiplayer_player_joins',
    'join_controller_to_mp_game', 'initialize_net_game_server_list',
    'start_net_game_server', 'dispose_net_game_server_list',
    'shutdown_net_game_server', 'net_game_join_from_server_list',
    'split_screen_game_initialize', 'coop_game_initialize',
    'main_menu_initialize', 'mp_type_menu_initialize',
    'pick_play_stage_for_quick_start', 'mp_level_list_initialize',
    'mp_level_list_dispose', 'mp_level_select', 'mp_profiles_list_initialize',
    'mp_profiles_list_dispose', 'mp_profile_set_for_game', 'swap_player_team',
    'net_game_join_player', 'player_profile_list_initialize',
    'player_profile_list_dispose',
    'wide_3_player_profile_set_for_game', 'wide_1_player_profile_set_for_game',
    'mp_profile_begin_editing', 'mp_profile_end_editing',
    'mp_profile_set_game_engine', 'mp_profile_change_name',
    'mp_profile_set_ctf_rules', 'mp_profile_set_koth_rules',
    'mp_profile_set_slayer_rules', 'mp_profile_set_oddball_rules',
    'mp_profile_set_racing_rules', 'mp_profile_set_player_options',
    'mp_profile_set_item_options', 'mp_profile_set_indicator_options',
    'mp_profile_init_game_engine', 'mp_profile_init_name',
    'mp_profile_init_ctf_rules', 'mp_profile_init_koth_rules',
    'mp_profile_init_slayer_rules', 'mp_profile_init_oddball_rules',
    'mp_profile_init_racing_rules', 'mp_profile_init_player_options',
    'mp_profile_init_item_options', 'mp_profile_init_indicator_options',
    'mp_profile_save_changes', 'color_picker_menu_initialize',
    'color_picker_menu_dispose', 'color_picker_select_color',
    'player_prof_begin_editing', 'player_prof_end_editing',
    'player_prof_change_name', 'player_prof_save_changes',
    'player_prof_init_control_settings', 'player_prof_init_adv_ctrl_settings',
    'player_prof_save_control_settings', 'player_prof_save_adv_ctrl_settings',
    'mp_game_player_quit', 'main_menu_switch_to_solo_game',
    'request_del_player_profile', 'request_del_playlist_profile',
    'final_del_player_profile', 'final_del_playlist_profile',
    'cancel_profile_delete',
    'create_and_edit_playlist_profile', 'create_and_edit_player_profile',
    'net_game_speed_start', 'net_game_delay_start',
    'net_server_accept_connection', 'net_server_defer_start',
    'net_server_allow_start', 'disable_if_no_xdemos', 'run_xdemos',
    'sp_reset_controller_choices',
    'sp_set_p1_controller_choices', 'sp_set_p2_controller_choices',
    'error_if_no_network_connection', 'start_server_if_none_advertised',
    'net_game_unjoin_player', 'close_if_not_editing_profile',
    'exit_to_xbox_dashboard', 'new_campaign_chosen', 'new_campaign_decision',
    'pop_history_stack_once', 'difficulty_menu_init', 'begin_music_fade_out',
    'new_game_if_no_player_profile', 'exit_gracefully_to_xbox_dashboard',
    'pause_game_invert_pitch', 'start_new_coop_game',
    'pause_game_invert_spinner_set', 'pause_game_invert_spinner_get',
    'main_menu_quit_game',
    'mouse_emit_ACCEPT_event', 'mouse_emit_BACK_event',
    'mouse_emit_DPAD_LEFT_event', 'mouse_emit_DPAD_RIGHT_event',
    'mouse_spinner_3wide_click',
    'controls_screen_init', 'video_screen_init', 'controls_begin_binding',
    'gamespy_screen_init', 'gamespy_screen_dispose',
    'gamespy_select_header', 'gamespy_select_item', 'gamespy_select_button',
    'player_prof_init_mouse_set', 'player_prof_change_mouse_set',
    'player_prof_init_audio_set', 'player_prof_change_audio_set',
    'player_prof_change_video_set',
    'controls_screen_dispose', 'controls_screen_change_set',
    'mouse_emit_X_event', 'gamepad_screen_init', 'gamepad_screen_dispose',
    'gamepad_screen_change_gamepads', 'gamepad_screen_select_item',
    'mouse_screen_defaults', 'audio_screen_defaults', 'video_screen_defaults',
    'controls_screen_defaults', 'profile_set_edit_begin',
    'profile_manager_delete', 'profile_manager_select',
    'gamespy_dismiiss_error', 'server_settings_init',
    'server_set_edit_server_name', 'server_set_edit_server_password', 
    'server_set_start_game', 'video_test_dialog_init',
    'video_test_dialog_dispose', 'video_test_dialog_accept',
    'gamespy_dismiss_filters', 'gamespy_update_filter_settings',
    'gamespy_dismiss_back_handler', 'mouse_spinner_1wide_click',
    'controls_back_handler', 'controls_advanced_launch', 'controls_advanced_ok',
    'mp_pause_menu_open', 'mp_game_options_open', 'mp_choose_team',
    'mp_prof_init_vehicle_options', 'mp_prof_save_vehicle_options',
    'single_prev_cl_item_active',
    'mp_prof_init_teamplay_options', 'mp_prof_save_teamplay_options',
    'mp_game_options_choose', 'emit_custom_activation_event',
    'player_prof_cancel_audio_set', 'player_prof_init_network_options',
    'player_prof_save_network_options', 'credits_post_render',
    'difficulty_item_select', 'credits_initialize', 'credits_dispose',
    'gamespy_get_patch', 'video_screen_dispose',
    'campaign_menu_init', 'campaign_menu_continue',
    'load_game_menu_init', 'load_game_menu_dispose', 'load_game_menu_activated',
    'solo_menu_save_checkpoint', 'mp_type_set_mode',
    'checking_for_updates_ok', 'checking_for_updates_dismiss',
    'direct_ip_connect_init', 'direct_ip_connect_go', 'direct_ip_edit_field',
    'network_settings_edit_a_port', 'network_settings_defaults',
    'load_game_menu_delete_request', 'load_game_menu_delete_finish'
    )

widget_bounds = QStruct("",
    SInt16("t"), SInt16("l"), SInt16("b"),  SInt16("r"),
    ORIENT='h', SIZE=8
    )

game_data_input = Struct("game_data_input",
    SEnum16("function", *game_data_input_functions),
    SIZE=36
    )

event_handler = Struct("event_handler",
    Bool32('flags',
        "close_current_widget",
        "close_other_widget",
        "close_all_widgets",
        "open_widget",
        "reload_self",
        "reload_other_widget",
        "give_focus_to_widget",
        "run_function",
        "replace_self_with_widget",
        "go_back_to_previous_widget",
        "run_scenario_script",
        "try_to_branch_on_failure",
        ),
    SEnum16("event_type", *event_types),
    SEnum16("function", *event_functions),
    dependency("widget_tag", "DeLa"),
    dependency("sound_effect", "snd!"),
    ascii_str32("script"),
    SIZE=72
    )

s_and_r_reference = Struct("search_and_replace_reference",
    ascii_str32("search_string"),
    SEnum16("replace_function",
        "NULL",
        "widgets_controller",
        "build_number",
        "pid",
        ),
    SIZE=34
    )

conditional_widget = Struct("conditional_widget",
    dependency("widget_tag", "DeLa"),
    ascii_str32("name"),  # UNUSED
    Bool32("flags",
        "load_if_event_handler_function_fails",
        ),
    SInt16("custom_controller_index"),  # UNUSED
    SIZE=80
    )

child_widget = Struct("child_widget",
    dependency("widget_tag", "DeLa"),
    ascii_str32("name"),  # UNUSED
    Bool32("flags",
        "use_custom_controller_index",
        ),
    SInt16("custom_controller_index"),
    SInt16("vertical_offset"),
    SInt16("horizontal_offset"),
    SIZE=80
    )

DeLa_body = Struct("tagdata",
    SEnum16("widget_type",
        "container",
        "text_box",
        "spinner_list",
        "column_list",
        "game_model",  # not implemented
        "movie",  # not implemented
        "custom"  # not implemented
        ),
    SEnum16("controller_index",
        "player_1",
        "player_2",
        "player_3",
        "player_4",
        "any_player"
        ),
    ascii_str32("name"),
    QStruct("bounds", INCLUDE=widget_bounds),
    Bool32('flags',
        "pass_unhandled_events_to_focused_child",
        "pause_game_time",
        "flash_background_bitmap",
        "dpad_up_down_tabs_thru_children",
        "dpad_left_right_tabs_thru_children",
        "dpad_up_down_tabs_thru_list_items",
        "dpad_left_right_tabs_thru_list_items",
        "dont_focus_a_specific_child_widget",
        "pass_unhandled_events_to_all_children",
        "return_to_main_menu_if_no_history",
        "always_use_tag_controller_index",
        "always_use_nifty_render_fx",
        "dont_push_history",
        "force_handle_mouse"
        ),
    SInt32("auto_close_time", SIDETIP="milliseconds"),
    SInt32("auto_close_fade_time", SIDETIP="milliseconds"),
    dependency("background_bitmap", "bitm"),

    reflexive("game_data_inputs", game_data_input, 64),
    reflexive("event_handlers", event_handler, 32),
    reflexive("search_and_replace_references",
              s_and_r_reference, 32, DYN_NAME_PATH='.search_string'),

    Pad(128),
    Struct("text_box",
        dependency("text_label_unicode_strings_list", "ustr"),
        dependency("text_font", "font"),
        QStruct("text_color", INCLUDE=argb_float),
        SEnum16("justification",
            "left",
            "right",
            "center",
            ),
        # as weird as it sounds, these flags are off alignment by 2
        Bool32("flags",
            "editable",
            "password",
            "flashing",
            "dont_do_that_weird_focus_test",
            ),
        BytesRaw("unknown2", SIZE=10, VISIBLE=False),

        FlSInt16("unknown3", VISIBLE=False),
        SInt16("string_list_index"),
        SInt16("horizontal_offset"),
        SInt16("vertical_offset")
        ),

    Pad(28),
    Struct("list_items",
        Bool32("flags",
            "list_items_generated_in_code",
            "list_items_from_string_list_tag",
            "list_items_only_one_tooltip",
            "list_single_preview_no_scroll"
            )
        ),

    Struct("spinner_list",
        dependency("list_header_bitmap", "bitm"),
        dependency("list_footer_bitmap", "bitm"),
        QStruct("header_bounds", INCLUDE=widget_bounds),
        QStruct("footer_bounds", INCLUDE=widget_bounds)
        ),

    Pad(32),
    Struct("column_list",
        dependency("extended_description_widget", "DeLa")
        ),

    Pad(288),
    reflexive("conditional_widgets", conditional_widget, 32,
        DYN_NAME_PATH='.widget_tag.filepath'),

    Pad(256),
    reflexive("child_widgets", child_widget, 32,
        DYN_NAME_PATH='.widget_tag.filepath'),

    SIZE=1004
    )

def get():
    return DeLa_def

DeLa_def = TagDef("DeLa",
    blam_header('DeLa'),
    DeLa_body,

    ext=".ui_widget_definition", endian=">", tag_cls=HekTag
    )
