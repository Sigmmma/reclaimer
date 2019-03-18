

# ########################################################################
# The element order in all the enumerators is important(DONT SHUFFLE THEM)
# ########################################################################

#Shared Enumerator options
materials_list = (
    "dirt",
    "sand",
    "stone",
    "snow",
    "wood",
    "metal_hollow",
    "metal_thin",
    "metal_thick",
    "rubber",
    "glass",
    "force_field",
    "grunt",
    "hunter_armor",
    "hunter_skin",
    "elite",
    "jackal",
    "jackal_energy_shield",
    "engineer_skin",
    "engineer_force_field",
    "flood_combat_form",
    "flood_carrier_form",
    "cyborg_armor",
    "cyborg_energy_shield",
    "human_armor",
    "human_skin",
    "sentinel",
    "moniter",
    "plastic",
    "water",
    "leaves",
    "elite_energy_shield",
    "ice",
    "hunter_shield",
    )
material_effect_types = (
    "walk",
    "run",
    "sliding",
    "shuffle",
    "jump",
    "jump_land",
    "biped_unused1",
    "biped_unused2",
    "impact",
    "vehicle_tire_slip",
    "vehicle_chassis_slip",
    "vehicle_unused1",
    "vehicle_unused2"
    )
object_types = (
    "obje",
    "bipd",
    "vehi",
    "weap",
    "eqip",
    "garb",
    "proj",
    "scen",
    "mach",
    "ctrl",
    "lifi",
    "plac",
    "ssce",
    )
actor_types = (
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
    "moniter",
    "sentinal",
    "none",
    "mounted_weapon"
    )
animation_functions = (
    "one",
    "zero",
    "cosine",
    "cosine_variable_period",
    "diagonal_wave",
    "diagonal_wave_variable_period",
    "slide",
    "slide_variable_period",
    "noise",
    "jitter",
    "wander",
    "spark",
    )
sound_volumes = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet"
    )
damage_category = (
    "none",
    "falling",
    "bullet",
    "grenade",
    "high_explosive",
    "sniper",
    "melee",
    "flame",
    "mounted_weapon",
    "vehicle",
    "plasma",
    "needle",
    "shotgun",
    )
grenade_types = (
    'human_frag',
    'covenant_plasma'
    )
fade_functions = (
    "linear",
    "early",
    "very_early",
    "late",
    "very_late",
    "cosine",
    )
detail_map_functions = (
    "double_biased_multiply",
    "multiply",
    "double_biased_add",
    )
device_functions = (
    "none",
    "power",
    "change_in_power",
    "position",
    "change_in_position",
    "locked",
    "delay",
    )
render_anchor = (
    "with_primary",
    "with_screen_space",
    "with_zsprite"
    )
render_fade_mode = (
    "none",
    "fade_when_perpendicular",
    "fade_when_parallel",
    )
render_mode = (
    "screen_facing",
    "parallel_to_direction",
    "perpendicular_to_direction"
    )
shader_flags = (
    "sort_bias",
    "nonlinear_tint",
    "dont_overdraw_fp_weapon"
    )
blend_flags = (
    "blend_in_hsv",
    "more_colors"
    )
hud_scaling_flags = (
    "dont_scale_offset",
    "dont_scale_size",
    "use_high_res_scale"
    )
hud_flash_flags = (
    "reverse_default_and_flashing_colors",
    )
hud_anchors = (
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "center"
    )
hud_panel_meter_flags = (
    "use_min_max_for_state_changes",
    "interpolate_between_min_max_flash_colors",
    "interpolate_color_along_hsv_space",
    "more_colors_for_hsv_interpolation ",
    "invert_interpolation"
    )
multitex_anchors = (
    "texture",
    "screen",
    )
multitex_wrap_modes = (
    "clamp",
    "wrap",
    )
blending_funcs = (
    "add",
    "subtract",
    "multiply",
    "multiply_2x",
    "dot",
    )
blend_functions = (
    "current",
    "next_map",
    "multiply",
    "double_multiply",
    "add",
    "add_signed_current",
    "add_signed_next_map",
    "subtract_signed_current",
    "subtract_signed_next_map",
    "blend_current_alpha",
    "blend_current_alpha_inverse",
    "blend_next_map_alpha",
    "blend_next_map_alpha_inverse",
    )
framebuffer_blend_functions = (
    "alpha_blend",
    "multiply",
    "double_multiply",
    "add",
    "subtract",
    "component_min",
    "component_max",
    "alpha_multiply_add",
    )

hmt_icon_types = (
    "a-button",
    "b-button",
    "x-button",
    "y-button",
    "black-button",
    "white-button",
    "left-trigger",
    "right-trigger",
    "dpad-up",
    "dpad-down",
    "dpad-left",
    "dpad-right",
    "start-button",
    "back-button",
    "left-thumb",
    "right-thumb",
    "left-stick",
    "right-stick",
    "action",
    "throw-grenade",
    "primary-trigger",
    "integrated-light",
    "jump",
    "use-equipment",
    "rotate-weapons",
    "rotate-grenades",
    "zoom",
    "crouch",
    "accept",
    "back",
    "move",
    "look",
    "custom-1",
    "custom-2",
    "custom-3",
    "custom-4",
    "custom-5",
    "custom-6",
    "custom-7",
    "custom-8",
    )
# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact lettering is important as the script extractor uses
# these strings to reconstruct scripts
script_types = (
    "startup",
    "dormant",
    "continuous",
    "static",
    "stub",
    )
script_object_types = (
    "unparsed",
    "special form",
    # built-in function type. function seems to
    # be specified by the index_union value, and
    # data value seems to always be 0
    "function name",
    "passthrough",
    "void",
    "boolean",
    "real",
    "short",
    "long", # 8

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS!
# The exact lettering is important as the script extractor
# uses these strings to reconstruct scripts

    "string",
    # lower 16bits of data points to entry in scripts
    "script", # 10

    # lower 16bits of data points to entry in their
    # respectively named arrays in the scenario. also,
    # cutscene_recording refers to recorded_animations.
    "trigger_volume",
    "cutscene_flag",
    "cutscene_camera_point",
    "cutscene_title",
    "cutscene_recording", # 15

    # lower 16bits of data points to entry in device groups
    "device_group",
    # lower 16bits of data points to entry in
    # encounters array, next 8bits points to entry
    # in squad array, and upper 8bits seem to be flags,
    # with the 8th bit signifying whether or not to
    # look in the squads array of the encounter.
    # specifies a squad if set, else an encounter.
    "ai",
    # lower 16bits of data points to entry in their
    # respectively named arrays in the scenario.
    "ai_command_list",
    "starting_profile",
    "conversation", # 20

    "navpoint",
    # lower 16bits of data points to entry in
    # messages array in scenario hud_messages
    "hud_message",
    "object_list", # 23

    # lower 16bits of data in all of these
    # points to a tag in the maps tag index
    "sound",
    "effect",
    "damage",
    "looping_sound",
    "animation_graph",
    "actor_variant",
    "damage_effect",
    "object_definition", # 31

    "game_difficulty",
    "team",
    "ai_default_state",
    # lower 16bits of data points to entry in bipeds palette
    # (yes, really, not the actors palette)
    "actor_type",
    "hud_corner", # 36

    # lower 16bits of data in all of these
    # points to entry in object names array
    "object",
    "unit",
    "vehicle",
    "weapon",
    "device",
    "scenery", # 42

    # lower 16bits of data in all of these
    # points to entry in object names array
    "object_name",
    "unit_name",
    "vehicle_name",
    "weapon_name",
    "device_name",
    "scenery_name", # 48
    )
# DO NOT MODIFY ANY OF THESE ENUMS!
# The exact lettering is important!
# INCOMPLETE: Entries with None haven't been determined yet.
# Additionally, some are duplicates. Not sure why, but they are
#    * == taken from script bible
#   ** == educated guess based on neighboring commands
script_built_in_functions = (
    "begin", # 0
    "begin_random",
    "if",
    "cond", # *
    "set",
    "and",
    "or",
    "+",
    "-",
    "*",
    "/", # 10
    "min", # *
    "max",
    "=",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
    "sleep",
    "sleep_until", # 20
    "wake",
    "inspect",
    "unit",
    "ai_debug_communication_supress", # *
    "ai_debug_communication_ignore", # *
    "ai_debug_communication_focus", # *
    "not",
    "print",
    "players",
    "volume_teleport_players_not_inside", # 30
    "volume_test_object",
    "volume_test_objects",
    "volume_test_objects_all",
    "object_teleport",
    "object_set_facing",
    "object_set_shield",
    "object_set_permutation",
    "object_create",
    "object_destroy",
    "object_create_anew", # 40
    "object_create_containing",
    "object_create_anew_containing",
    "object_destroy_containing",
    "object_destroy_all",
    "list_get",
    "list_count",
    "effect_new",
    "effect_new_on_object_marker",
    "damage_new",
    "damage_object", # 50
    "objects_can_see_object",
    "objects_can_see_flag",
    "objects_delete_by_definition",
    None,
    # these next 5 might be shifted. a little
    "sound_set_gain", # *
    "sound_set_gain", # * same as previous, but extra arg
    "script_recompile", # *
    "help", # *
    "random_range", # *
    "real_random_range", # 60
    "numeric_countdown_timer_set",
    "numeric_countdown_timer_get", # *
    "numeric_countdown_timer_stop",
    "numeric_countdown_timer_restart", # *
    "breakable_surfaces_enable",
    "recording_play",
    "recording_play_and_delete",
    "recording_play_and_hover",
    "recording_kill",
    "recording_time", # 70
    "object_set_ranged_attack_inhibited",
    "object_set_melee_attack_inhibited",
    "objects_dump_memory", # *
    "object_set_collideable",
    "object_set_scale",
    "objects_attach",
    "objects_detach",
    "garbage_collect_now",
    "object_cannot_take_damage",
    "object_can_take_damage", # 80
    "object_beautify",
    "objects_predict",
    "object_type_predict",
    "object_pvs_activate",
    "object_pvs_set_object",
    "object_pvs_set_camera",
    "object_pvs_clear",
    "render_lights",
    "scenery_get_animation_time", # *
    "scenery_animation_start", # 90
    "scenery_animation_start_at_frame",
    "render_effects", # *
    "unit_can_blink", # *
    "unit_open",
    "unit_close",
    "unit_kill",
    "unit_kill_silent", # *
    "unit_get_custom_animation_time",
    "unit_stop_custom_animation",
    "unit_custom_animation_at_frame", # 100
    "custom_animation",
    "custom_animation_list",
    "unit_is_playing_custom_animation",
    "unit_aim_without_turning", # *
    "unit_set_emotion",
    "unit_set_enterable_by_player",
    "unit_enter_vehicle",
    "vehicle_test_seat_list",
    "vehicle_test_seat",
    "unit_set_emotion_animation", # * 110
    "unit_exit_vehicle",
    "unit_set_maximum_vitality",
    "units_set_maximum_vitality", # *
    "unit_set_current_vitality",
    "units_set_current_vitality",
    "vehicle_load_magic",
    "vehicle_unload",
    "magic_seat_name", # *
    "unit_set_seat",
    "magic_melee_attack", # * 120
    "vehicle_riders",
    "vehicle_driver", # *
    "vehicle_gunner",
    "unit_get_health",
    "unit_get_shield",
    "unit_get_total_grenade_count",
    "unit_has_weapon",
    "unit_has_weapon_readied",
    "unit_doesnt_drop_items",
    "unit_impervious", # 130
    "unit_suspended",
    "unit_solo_player_integrated_night_vision_is_active",
    "units_set_desired_flashlight_state",
    "unit_set_desired_flashlight_state",
    "unit_get_current_flashlight_state",
    "device_set_never_appears_locked",
    "device_get_power",
    "device_set_power",
    "device_set_position",
    "device_get_position", # 140
    "device_set_position_immediate",
    "device_group_get",
    "device_group_set",
    "device_group_set_immediate",
    "device_one_sided_set",
    "device_operates_automatically_set",
    "device_group_change_only_once_more_set",
    "breakable_surfaces_reset",
    "cheat_all_powerups", # *
    "cheat_all_weapons", # * 150
    "cheat_spawn_warthog", # *
    "cheat_all_vehicles", # *
    "cheat_teleport_to_camera", # *
    "cheat_active_camouflage", # *
    # no space for this command. Might not actually exist
    #"cheat_active_camouflage_local_player", # *
    "cheats_load", # *
    "ai_free",
    "ai_free_units",
    "ai_attach",
    "ai_attach",
    "ai_detach", # 160
    "ai_place",
    "ai_place",
    "ai_kill",
    "ai_kill_silent",
    "ai_erase",
    "ai_erase_all",
    "ai_select", # *
    # no space for this command. Might not actually exist
    #"ai_deselect", # *
    "ai_spawn_actor",
    "ai_spawn_actor",
    "ai_set_deaf", # 170
    "ai_set_blind",
    "ai_magically_see_encounter",
    "ai_magically_see_encounter",
    "ai_magically_see_players",
    "ai_magically_see_unit", # *
    "ai_timer_expire",
    "ai_attack",
    "ai_attack",
    "ai_retreat",
    "ai_maneuver", # 180
    "ai_maneuver",
    "ai_migrate",
    "ai_migrate",
    "ai_migrate_and_speak",
    "ai_migrate_by_unit",
    "ai_allegiance",
    "ai_living_count",
    "ai_living_count",
    "ai_strength",
    "ai_strength", # 190
    "ai_nonswarm_count",
    "ai_nonswarm_count",
    "ai_actors",
    "ai_go_to_vehicle",
    "ai_going_to_vehicle",
    "ai_exit_vehicle",
    "ai_braindead",
    "ai_braindead",
    "ai_braindead_by_unit",
    "ai_prefer_target", # 200
    "ai_teleport_to_starting_location",
    "ai_teleport_to_starting_location_if_unsupported",
    "ai_teleport_to_starting_location_if_unsupported",
    "ai_renew",
    "ai_try_to_fight",
    "ai_try_to_fight",
    "ai_try_to_fight_player",
    "ai_command_list",
    "ai_command_list_by_unit",
    "ai_command_list_advance", # 210
    "ai_command_list_status",
    "ai_command_list_status",
    "ai_force_active",
    "ai_force_active",
    "ai_set_return_state", # *
    "ai_set_current_state", # *
    "ai_playfight",
    "ai_playfight",
    "ai_status",
    "ai_vehicle_encounter", # 220
    "ai_vehicle_enterable_distance",
    "ai_vehicle_enterable_distance",
    "ai_vehicle_enterable_actor_type",
    "ai_vehicle_enterable_actors", # *
    "ai_vehicle_enterable_disable",
    "ai_look_at_object", # *
    "ai_stop_looking", # *
    "ai_automatic_migration_target",
    "ai_automatic_migration_target",
    "ai_follow_target_disable", # 230
    "ai_follow_target_players",
    "ai_follow_target_ai",
    "ai_follow_distance",
    "ai_conversation",
    "ai_conversation",
    "ai_conversation_stop",
    "ai_conversation_advance",
    "ai_conversation_status",
    "ai_conversation_status",
    "ai_link_activation", # 240
    "ai_berserk",
    "ai_set_team",
    "ai_allow_dormant",
    "ai_allow_dormant",
    "ai_allegiance_broken",
    "camera_control",
    "camera_set",
    "camera_set_relative",
    "camera_set_first_person",
    "camera_set_dead", # 250
    "camera_set_dead",
    "camera_time",
    "debug_camera_load",
    "debug_camera_save",
    "game_speed",
    "game_variant", # *
    "game_difficulty_get",
    "game_difficulty_get",
    "game_difficulty_get_real",
    "profile_service_clear_timers", # * 260
    "profile_service_dump_timers", # *
    "map_reset",
    "map_name",
    "switch_bsp",
    "structure_bsp_index",
    "crash", # *
    "switch_bsp",
    "structure_bsp_index",
    "version", # *
    "playback", # * 270
    "quit", # *
    "texture_cache_flush", # *
    "sound_cache_flush", # *
    "sound_cache_dump_to_file", # *
    "debug_memory", # *
    "debug_memory_by_file", # *
    "debug_memory_for_file", # *
    "debug_tags", # *
    "profile_reset", # *
    "profile_dump", # *280
    # no space for these commands. Might not actually exist
    #"profile_activate", # *
    #"profile_deactivate", # *
    #"profile_graph_toggle", # *
    "debug_pvs", # *
    "radiosity_start", # *
    # no space for these commands. Might not actually exist
    #"radiosity_save", # *
    #"radiosity_debug_point", # *
    "ai",
    "ai_dialogue_triggers",
    "ai_grenades",
    None, None,
    "ai",
    "ai_dialogue_triggers",
    "ai_grenades", # 290
    None,
    "fade_in",
    "fade_out",
    "cinematic_start",
    "cinematic_stop",
    "cinematic_skip_start_internal",
    "fade_in",
    "fade_out",
    "cinematic_start",
    "cinematic_stop", # 300
    "cinematic_suppress_bsp_object_creation",
    "cinematic_skip_start_internal",
    "cinematic_skip_stop_internal",
    "cinematic_show_letterbox",
    "cinematic_set_title",
    "game_all_quiet",
    "game_safe_to_speak",
    "game_is_cooperative",
    "game_won",
    "game_lost", # 310
    "game_safe_to_save",
    "game_save_totally_unsafe",
    "game_saving",
    "game_is_cooperative",
    "game_reverted",
    "game_save_cancel",
    "game_save_no_timeout",
    "game_save_totally_unsafe",
    "game_saving",
    "game_revert", # 320
    "game_reverted",
    "game_skip_ticks",
    "sound_impulse_start",
    "sound_impulse_time",
    "sound_impulse_stop",
    "sound_looping_start",
    "sound_looping_start",
    "game_skip_ticks",
    "sound_looping_set_alternate",
    "sound_impulse_start", # 330
    "sound_impulse_time",
    "sound_impulse_stop",
    "sound_looping_predict", # *
    "sound_looping_start",
    "sound_looping_stop",
    "vehicle_hover",
    "sound_looping_set_alternate",
    "player_enable_input",
    "player_camera_control",
    "player_action_test_reset", # 340
    "player_action_test_jump", # *
    "player_action_test_primary_trigger",
    "player_action_test_grenade_trigger",
    "player_action_test_zoom", # *
    "player_action_test_action",
    "player_action_test_accept",
    "player_action_test_back",
    "sound_class_set_gain",
    "vehicle_hover",
    "players_unzoom_all", # 350
    "player_enable_input",
    "player_action_test_look_relative_all_directions",
    "player_action_test_reset",
    "player_add_equipment",
    "show_hud",
    "show_hud",
    "show_hud_help_text",
    "enable_hud_help_flash",
    "hud_help_flash_restart", # *
    "activate_nav_point_flag", # *360
    # no space for this command. Might not actually exist
    #"activate_nav_point_object", # *
    "activate_team_nav_point_flag",
    "activate_team_nav_point_flag",
    "activate_team_nav_point_object",
    "deactivate_nav_point_flag", # *
    # no space for this command. Might not actually exist
    #"deactivate_nav_point_object", # *
    "deactivate_team_nav_point_flag",
    "deactivate_team_nav_point_flag",
    "deactivate_team_nav_point_object",
    "cls",
    "show_hud",
    "show_hud_help_text", # 370
    "player_effect_set_max_translation",
    "player_effect_set_max_rotation",
    "player_effect_set_max_rumble",
    "player_effect_start",
    "activate_team_nav_point_flag",
    "activate_team_nav_point_object",
    "hud_blink_health",
    "hud_show_shield",
    "deactivate_team_nav_point_flag",
    "deactivate_team_nav_point_object", # 380
    "hud_blink_motion_sensor",
    "hud_show_crosshair",
    "hud_set_help_text",
    "hud_set_help_text",
    "hud_set_objective_text",
    "hud_set_timer_time",
    "hud_set_timer_warning_time",
    "hud_set_timer_position",
    "show_hud_timer",
    "pause_hud_timer", # 390
    "hud_get_timer_ticks",
    "time_code_show",
    "time_code_start",
    "time_code_reset", # *
    None, None,
    "rasterizer_model_ambient_reflection_tint",
    "rasterizer_lights_reset_for_new_map",
    "cinematic_screen_effect_start",
    "player_effect_set_max_translation", # 400
    "player_effect_set_max_rotation",
    "player_effect_set_max_rumble",
    "player_effect_start",
    "player_effect_stop",
    "cinematic_screen_effect_stop",
    "cinematic_set_near_clip_distance",
    "hud_show_shield",
    "hud_show_health", # **
    "hud_show_motion_sensor",
    "hud_show_crosshair", # ** 410
    "player0_look_invert_pitch",
    "player0_look_pitch_is_inverted",
    "hud_set_help_text",
    "hud_set_objective_text",
    "display_scenario_help",
    None, None, None, None,
    None, # 420
    None, None, None, None, None, None, None,
    "rasterizer_decals_flush",
    "rasterizer_fps_accumulate", # *
    "rasterizer_model_ambient_reflection_tint", # 430
    "rasterizer_lights_reset_for_new_map", # *
    "script_screen_effect_set_value", # *
    "cinematic_screen_effect_start",
    "cinematic_screen_effect_set_convolution",
    "cinematic_screen_effect_set_filter",
    "cinematic_screen_effect_set_filter_desaturation_tint",
    "cinematic_screen_effect_set_video", # *
    "cinematic_screen_effect_stop",
    None,
    None, # 440
    None, None, None, None, None, None, None, None, None,
    None, # 450
    None, None, None, None, None, None, None, None, None,
    None, # 460
    None, None, None, None, None, None, None, None, None,
    None, # 470
    None, None, None, None, None, None, None, None, None,
    None, # 480
    None, None, None, None, None, None, None, None, None,
    None, # 490
    None, None, None, None, None, None, None, None, None,
    None, # 500
    None, None, None, None, None,
    "sv_say",
    None, None, None,
    None, # 510
    None, None, None, None, None, None, None, None, None,
    None, # 520
    None, None, None, None, None, None, None, None, None,
    None, # 530
    None, None, None, None, None, None, None, None, None,
    None, # 540
    None, None, None, None, None, None, None, None, None,
    None, # 550
    None, None,
    # OPEN SAUCE SHEET
    "objects_distance_to_object",
    "object_data_get_real",
    "object_data_set_real",
    "weapon_data_get_real",
    "weapon_data_set_real",
    "weapon_data_trigger_set_real",
    None,
    "unit_data_get_integer", # 560
    "unit_data_get_object",
    "unit_data_get_integer",
    "unit_data_set_integer",
    "unit_data_get_real",
    "unit_data_set_real",
    "physics_get_gravity", # *
    "physics_set_gravity",
    "physics_constants_reset", # *
    "physics_get_gravity", # *
    None, None,
    None, # 570
    None, None, None, None, None, None, None,
    "abs_integer", # *
    "abs_real",
    None, # 580
    "pp_get_effect_instance_index_by_name", # * 580
    "pp_set_effect_instance_active",
    "pp_set_effect_instance_fade",
    "pp_set_effect_instance_active",
    "pp_set_effect_instance_fade",
    None,
    "pp_get_effect_is_valid",
    "pp_get_effect_shader_variable_index_by_name", # *
    "pp_set_effect_shader_variable_boolean",
    "pp_set_effect_shader_variable_integer", # *
    "pp_set_effect_shader_variable_real", # * 590
    "pp_set_effect_shader_instance_active", # *
    "pp_bloom_set_size", # *
    "pp_bloom_set_exposure",
    "pp_bloom_set_mix_amount",
    "pp_bloom_set_exposure",
    "pp_bloom_set_mix_amount",
    "pp_bloom_set_minimum_color", # *
    "pp_bloom_set_maximum_color", # *
    "bitwise_and", # *
    "bitwise_or", # *600
    "bitwise_xor", # *
    "bitwise_lhs", # *
    "bitwise_rhs", # *
    "bit_test",
    "bit_toggle",
    "bit_flags_test", # *
    "bit_flags_toggle", # *
    None, None,
    None, # 610
    "runtime_vector_get_element",
    "runtime_vector_set_element",
    "runtime_vector_set",
    "runtime_vector_operation",
    "runtime_vector_to_string", # *
    "object_data_set_vector",
    "object_data_save_vector",
    "display_scripted_ui_widget",
    "play_bink_movie", # *
    "hex_string_to_long", # * 620
    None, None, None,
    "structure_bsp_set_lightmap_set",
    "structure_bsp_set_sky_set",
    "ai_transforms_enabled", # *
    "ai_transform_actors",
    "ai_transform_actors_by_type", # *
    "ai_actor_is_transforming", # *
    )
_script_built_in_functions_test = list(script_built_in_functions)
#print("Current number of valid built-in script functions: %s" %
#      sum(i is not None for i in _script_built_in_functions_test))

def TEST_PRINT_HSC_BUILT_IN_FUNCTIONS():
    i = 0
    for string in _script_built_in_functions_test:
        if string is None:
            print('    None,', end="")
        else:
            print('    "%s",' % string, end="")

        if not (i % 10):
            print(" # %s" % i, end="")
        print()
        i += 1

    print("Current number of valid built-in script functions: %s" %
          sum(i is not None for i in script_built_in_functions))


function_names = (
    "none",
    "A",
    "B",
    "C",
    "D",
    )
function_inputs_outputs = (
    "none",
    "A_in",
    "B_in",
    "C_in",
    "D_in",
    "A_out",
    "B_out",
    "C_out",
    "D_out",
    )
function_inputs = (
    "none",
    "A_in",
    "B_in",
    "C_in",
    "D_in",
    )
function_outputs = (
    "none",
    "A_out",
    "B_out",
    "C_out",
    "D_out",
    )
#Tag class specific enumerators
object_export_to = (
    'none',
    'body_vitality',
    'shield_vitality',
    'recent_body_damage',
    'recent_shield_damage',
    'random_constant',
    'umbrella_shield_vitality',
    'shield_stun',
    'recent_umbrella_shield_vitality',
    'umbrella_shield_stun',
    'region_0_damage',
    'region_1_damage',
    'region_2_damage',
    'region_3_damage',
    'region_4_damage',
    'region_5_damage',
    'region_6_damage',
    'region_7_damage',
    'alive',
    'compass',
    )
weapon_export_to = (
    'none',
    'heat',
    'primary_ammunition',
    'secondary_ammunition',
    'primary_rate_of_fire',
    'secondary_rate_of_fire',
    'ready',
    'primary_ejection_port',
    'secondary_ejection_port',
    'overheated',
    'primary_charged',
    'secondary_charged',
    'illumination',
    'age',
    'integrated_light',
    'primary_firing',
    'secondary_firing',
    'primary_firing_on',
    'secondary_firing_on',
    )
biped_inputs = (
    'none',
    'flying_velocity'
    )
projectile_inputs = (
    "none",
    "range_remaining",
    "time_remaining",
    "tracer",
    )
unit_inputs = (
    "none",
    "driver_seat_power",
    "gunner_seat_power",
    "aiming_change",
    "mouth_aperture",
    "integrated_light_power",
    "can_blink",
    "shield_sapping"
    )
unit_teams = (
    "none",
    "player",
    "human",
    "covenant",
    "flood",
    "sentinel",
    "unused6",
    "unused7",
    "unused8",
    "unused9",
    )
vehicle_inputs = (
    "none",
    "speed_absolute",
    "speed_forward",
    "speed_backward",
    "slide_absolute",
    "slide_left",
    "slide_right",
    "speed_slide_maximum",
    "turn_absolute",
    "turn_left",
    "turn_right",
    "crouch",
    "jump",
    "walk",
    "velocity_air",
    "velocity_water",
    "velocity_ground",
    "velocity_forward",
    "velocity_left",
    "velocity_up",
    "left_tread_position",
    "right_tread_position",
    "left_tread_velocity",
    "right_tread_velocity",
    "front_left_tire_position",
    "front_right_tire_position",
    "back_left_tire_position",
    "back_right_tire_position",
    "front_left_tire_velocity",
    "front_right_tire_velocity",
    "back_left_tire_velocity",
    "back_right_tire_velocity",
    "wingtip_contrail",
    "hover",
    "thrust",
    "engine_hack",
    "wingtip_contrail_new",
    )
vehicle_types = (
    "human_tank",
    "human_jeep",
    "human_boat",
    "human_plane",
    "alien_scout",
    "alien_fighter",
    "turret",
    )
weapon_types = (
    "undefined",
    "shotgun",
    "needler",
    "plasma_pistol",
    "plasma_rifle",
    )
trans_shdr_properties = (
    "alpha_tested",
    "decal",
    "two_sided",
    "first_map_is_in_screenspace",
    "draw_before_water",
    "ignore_effect",
    "scale_first_map_with_distance",
    "numeric",
    )
trans_shdr_first_map_type = (
    "map_2d",
    "reflection_cube_map",
    "object_centered_cube_map",
    "viewer_centered_cube_map",
    )
detail_mask = (
    "none",
    "reflection_mask_inverse",
    "reflection_mask",
    "self_illumination_mask_inverse",
    "self_illumination_mask",
    "color_change_mask_inverse",
    "color_change_mask",
    "auxiliary_mask_inverse",
    "auxiliary_mask"
    )
anim_types = (
    "base",
    "overlay",
    "replacement"
    )
anim_frame_info_types = (
    "none",
    "dx,dy",
    "dx,dy,dyaw",
    "dx,dy,dz,dyaw",
    )


# ########################################################################
# The element order in all the enumerators is important(DONT SHUFFLE THEM)
# ########################################################################

#Shared Enumerator options
grenade_types_os = (
    'human frag',
    'covenant plasma',
    'custom 2',
    'custom 3',
    )

actor_states = (
    'none',
    'sleeping',
    'alert',
    'moving repeat same position',
    'moving loop',
    'moving loop back and forth',
    'moving loop randomly',
    'moving randomly',
    'guarding',
    'guarding at guard position',
    'searching',
    'fleeing'
    )
