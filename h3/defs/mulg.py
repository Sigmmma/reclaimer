############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	named plugins
# revision: 3		author: OrangeMohawk
# 	Standardized Event Reflexives
# revision: 4		author: Lord Zedd
# 	Updating
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

mulg_runtime_assault_event_event = (
    "game_start",
    "bomb_taken",
    "bomb_dropped",
    "bomb_returned_by_player",
    "bomb_returned_by_timeout",
    "bomb_captured",
    "bomb_new_defensive_team",
    "bomb_return_failure",
    "side_switch_tick",
    "side_switch_final_tick",
    "side_switch_30_seconds",
    "side_switch_10_seconds",
    "bomb_returned_by_defusing",
    "bomb_placed_on_enemy_post",
    "bomb_arming_started",
    "bomb_arming_completed",
    "bomb_contested",
    "bomb_returned_neutral",
    )

mulg_runtime_ctf_event_event = (
    "game_start",
    "flag_taken",
    "flag_taken_2",
    "flag_dropped",
    "flag_returned_by_player",
    "flag_returned_by_timeout",
    "flag_captured",
    "flag_new_defensive_team",
    "flag_return_failure",
    "side_switch_tick",
    "side_switch_final_tick",
    "side_switch_30_seconds",
    "side_switch_10_seconds",
    "flag_contested",
    "flag_capture_failure",
    )

mulg_runtime_flavor_event_event = (
    "extermination",
    "perfection",
    "double_kill",
    "triple_kill",
    "overkill",
    "killtacular",
    "killtrocity",
    "killimanjaro",
    "killtastrophe",
    "killpocalypse",
    "killionaire",
    "killing_spree",
    "killing_frenzy",
    "running_riot",
    "rampage",
    "untouchable",
    "invincible",
    "sniper_spree",
    "sharpshooter",
    "shotgun_spree",
    "open_season",
    "splatter_spree",
    "vehicular_manslaughter",
    "sword_spree",
    "slice_n_dice",
    "juggernaut_spree",
    "unstoppable",
    "infection_spree",
    "mmmm_brains",
    "zombie_killing_spree",
    "hell_s_janitor",
    "is_quisnam_protero_damno",
    "hail_to_the_king",
    "bulltrue",
    "splatter",
    "highjack",
    "skyjack",
    "death_from_the_grave",
    "killjoy",
    "laser_kill",
    "sticky_kill",
    "sniper_kill",
    "assassin",
    "beat_down",
    "incineration",
    "wheelman",
    "bomb_planted",
    "killed_bomb_carrier",
    "killed_vip",
    "killed_juggernaut",
    "oddball_kill",
    "flag_score",
    "killed_flag_carrier",
    "flag_kill",
    "last_man_standing",
    "sandbox_not_enough_room",
    "sandbox_too_many_on_map",
    )

mulg_runtime_general_event_audience = (
    "cause_player",
    "cause_team",
    "effect_player",
    "effect_team",
    "all",
    )

mulg_runtime_general_event_event = (
    "kill",
    "suicide",
    "betrayal",
    "victory",
    "team_victory",
    "unused1",
    "unused2",
    "_1_min_to_win",
    "team_1_min_to_win",
    "_30_secs_to_win",
    "team_30_secs_to_win",
    "player_quit",
    "player_joined",
    "killed_by_unknown",
    "_30_minutes_left",
    "_15_minutes_left",
    "_5_minutes_left",
    "_1_minute_left",
    "time_expired",
    "game_over",
    "respawn_tick",
    "last_respawn_tick",
    "teleporter_used",
    "teleporter_blocked",
    "player_changed_team",
    "player_rejoined",
    "gained_lead",
    "gained_team_lead",
    "lost_lead",
    "lost_team_lead",
    "tied_leader",
    "tied_team_leader",
    "round_over",
    "_30_seconds_left",
    "_10_seconds_left",
    "kill_falling",
    "kill_collision",
    "kill_melee",
    "sudden_death",
    "player_booted_player",
    "kill_flag_carrier",
    "kill_bomb_carrier",
    "kill_sticky_grenade",
    "kill_sniper",
    "kill_standard_melee",
    "boarded_vehicle",
    "start_team_notice",
    "telefrag",
    "_10_secs_to_win",
    "team_10_secs_to_win",
    "kill_bulltrue",
    "kill_post_mortem",
    "highjack",
    "skyjack",
    "kill_laser",
    "kill_fire",
    "wheelman",
    )

mulg_runtime_general_event_required_field = (
    "none",
    "cause_player",
    "cause_team",
    "effect_player",
    "effect_team",
    )

mulg_runtime_general_event_team = (
    "none_player_only",
    "cause",
    "effect",
    "all",
    )

mulg_runtime_general_event_type = (
    "general",
    "flavor",
    "slayer",
    "capture_the_flag",
    "oddball",
    "unused",
    "king_of_the_hill",
    "vip",
    "juggernaut",
    "territories",
    "assault",
    "infection",
    )

mulg_runtime_infection_event_event = (
    "game_start",
    "infected",
    "new_zombie",
    "new_alpha_zombie",
    "last_man_standing",
    )

mulg_runtime_juggernaut_event_event = (
    "game_start",
    "new_juggernaut",
    "destination_move",
    "juggernaut_killed",
    )

mulg_runtime_king_of_the_hill_event_event = (
    "game_start",
    "hill_controlled",
    "hill_contested",
    "hill_tick",
    "hill_move",
    "hill_controlled_team",
    "hill_contested_team",
    )

mulg_runtime_oddball_event_event = (
    "game_start",
    "ball_spawned",
    "ball_picked_up",
    "ball_dropped",
    "ball_reset",
    "ball_tick",
    "_10_points_remaining",
    "_25_points_remaining",
    )

mulg_runtime_slayer_event_event = (
    "game_start",
    "new_target",
    )

mulg_runtime_state_response_state = (
    "waiting_for_space_to_clear",
    "observing",
    "respawning_soon",
    "sitting_out",
    "out_of_lives",
    "playing_winning",
    "playing_tied",
    "playing_losing",
    "game_over_won",
    "game_over_tied",
    "game_over_lost",
    "game_over_tied2",
    "you_have_flag",
    "enemy_has_flag",
    "flag_not_home",
    "carrying_oddball",
    "you_are_juggernaut",
    "you_control_hill",
    "switching_sides_soon",
    "player_recently_started",
    "you_have_bomb",
    "flag_contested",
    "bomb_contested",
    "limited_lives_multiple",
    "limited_lives_single",
    "limited_lives_final",
    "playing_winning_unlimited",
    "playing_tied_unlimited",
    "playing_losing_unlimited",
    )

mulg_runtime_territories_event_event = (
    "game_start",
    "territory_control_gained",
    "territory_contest_lost",
    "all_territories_controlled",
    "new_defensive_team",
    )

mulg_runtime_vip_event_event = (
    "game_start",
    "new_vip",
    "killed_vip",
    "vip_death",
    "vip_notice",
    "arrived_at_destination",
    "destination_move",
    )


mulg_universal_team_color = Struct("team_color", 
    color_rgb_float("color"),
    ENDIAN=">", SIZE=12
    )


mulg_universal_armor_customization_region_permuation_variant = Struct("variant", 
    h3_string_id("region"),
    h3_string_id("permutation"),
    ENDIAN=">", SIZE=8
    )


mulg_universal_armor_customization_region_permuation = Struct("permuation", 
    h3_string_id("name"),
    h3_string_id("description"),
    Bool16("flags", 
        "has_requirement",
        "has_special_requirement",
        ),
    SInt16("unknown"),
    h3_string_id("achievement_requirement"),
    h3_reflexive("variant", mulg_universal_armor_customization_region_permuation_variant),
    ENDIAN=">", SIZE=28
    )


mulg_universal_armor_customization_region = Struct("region", 
    h3_string_id("name"),
    h3_reflexive("permuations", mulg_universal_armor_customization_region_permuation),
    ENDIAN=">", SIZE=16
    )


mulg_universal_armor_customization = Struct("armor_customization", 
    h3_string_id("character_name"),
    h3_reflexive("regions", mulg_universal_armor_customization_region),
    ENDIAN=">", SIZE=16
    )


mulg_universal_game_variant_weapon = Struct("game_variant_weapon", 
    h3_string_id("name"),
    Float("random_chance"),
    h3_dependency("weapon"),
    ENDIAN=">", SIZE=24
    )


mulg_universal_game_variant_vehicle = Struct("game_variant_vehicle", 
    h3_string_id("name"),
    h3_dependency("vehicle"),
    ENDIAN=">", SIZE=20
    )


mulg_universal_game_variant_equipment = Struct("game_variant_equipment", 
    h3_string_id("name"),
    h3_dependency("grenade"),
    ENDIAN=">", SIZE=20
    )


mulg_universal_weapon_set_substitution = Struct("substitution", 
    h3_string_id("original_weapon"),
    h3_string_id("substituted_weapon"),
    ENDIAN=">", SIZE=8
    )


mulg_universal_weapon_set = Struct("weapon_set", 
    h3_string_id("name"),
    h3_reflexive("substitutions", mulg_universal_weapon_set_substitution),
    ENDIAN=">", SIZE=16
    )


mulg_universal_vehicle_set_substitution = Struct("substitution", 
    h3_string_id("original_vehicle"),
    h3_string_id("substituted_vehicle"),
    ENDIAN=">", SIZE=8
    )


mulg_universal_vehicle_set = Struct("vehicle_set", 
    h3_string_id("name"),
    h3_reflexive("substitutions", mulg_universal_vehicle_set_substitution),
    ENDIAN=">", SIZE=16
    )


mulg_universal = Struct("universal", 
    h3_dependency("random_player_name_strings"),
    h3_dependency("team_name_strings"),
    h3_reflexive("team_colors", mulg_universal_team_color),
    h3_reflexive("armor_customization", mulg_universal_armor_customization),
    h3_dependency("multiplayer_strings"),
    h3_dependency("sandbox_ui_strings"),
    h3_dependency("sandbox_ui_properties"),
    h3_reflexive("game_variant_weapons", mulg_universal_game_variant_weapon),
    h3_reflexive("game_variant_vehicles", mulg_universal_game_variant_vehicle),
    h3_reflexive("game_variant_equipment", mulg_universal_game_variant_equipment),
    h3_reflexive("weapon_sets", mulg_universal_weapon_set),
    h3_reflexive("vehicle_sets", mulg_universal_vehicle_set),
    h3_dependency("engine_settings"),
    ENDIAN=">", SIZE=180
    )


mulg_runtime_sound = Struct("sound", 
    h3_dependency("sound"),
    ENDIAN=">", SIZE=16
    )


mulg_runtime_looping_sound = Struct("looping_sound", 
    h3_dependency("looping_sound"),
    ENDIAN=">", SIZE=16
    )


mulg_runtime_general_event = Struct("general_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_general_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_flavor_event = Struct("flavor_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_flavor_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_slayer_event = Struct("slayer_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_slayer_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_ctf_event = Struct("ctf_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_ctf_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_oddball_event = Struct("oddball_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_oddball_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_king_of_the_hill_event = Struct("king_of_the_hill_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_king_of_the_hill_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_vip_event = Struct("vip_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_vip_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_juggernaut_event = Struct("juggernaut_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_juggernaut_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_territories_event = Struct("territories_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_territories_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_assault_event = Struct("assault_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_assault_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_infection_event = Struct("infection_event", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *mulg_runtime_general_event_type),
    SEnum16("event", *mulg_runtime_infection_event_event),
    SEnum16("audience", *mulg_runtime_general_event_audience),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SEnum16("team", *mulg_runtime_general_event_team),
    SInt16("unknown_2", VISIBLE=False),
    h3_string_id("display_string"),
    h3_string_id("display_medal"),
    SEnum16("required_field", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience", *mulg_runtime_general_event_required_field),
    SEnum16("required_field_2", *mulg_runtime_general_event_required_field),
    SEnum16("excluded_audience_2", *mulg_runtime_general_event_required_field),
    h3_string_id("primary_string"),
    SInt32("primary_string_duration"),
    h3_string_id("plural_display_string"),
    Float("sound_delay_announcer_only"),
    Bool16("sound_flags", 
        "announcer_sound",
        ),
    SInt16("unknown_3", VISIBLE=False),
    h3_dependency("english_sound"),
    h3_dependency("japanese_sound"),
    h3_dependency("german_sound"),
    h3_dependency("french_sound"),
    h3_dependency("spanish_sound"),
    h3_dependency("latin_american_spanish_sound"),
    h3_dependency("italian_sound"),
    h3_dependency("korean_sound"),
    h3_dependency("chinese_traditional_sound"),
    h3_dependency("chinese_simplified_sound"),
    h3_dependency("portuguese_sound"),
    h3_dependency("polish_sound"),
    BytesRaw("unknown_4", SIZE=16, VISIBLE=False),
    ENDIAN=">", SIZE=260
    )


mulg_runtime_multiplayer_constant_weapon = Struct("weapon", 
    h3_dependency("weapon", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


mulg_runtime_multiplayer_constant_vehicle = Struct("vehicle", 
    h3_dependency("vehicle", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


mulg_runtime_multiplayer_constant_projectile = Struct("projectile", 
    h3_dependency("projectile", VISIBLE=False),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=28
    )


mulg_runtime_multiplayer_constant_equipment = Struct("equipment", 
    h3_dependency("equipment", VISIBLE=False),
    Float("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


mulg_runtime_multiplayer_constant = Struct("multiplayer_constant", 
    Array("unknown_array_0", SUB_STRUCT=Float("unknown"), SIZE=26, VISIBLE=False),
    h3_reflexive("weapons", mulg_runtime_multiplayer_constant_weapon),
    h3_reflexive("vehicles", mulg_runtime_multiplayer_constant_vehicle),
    h3_reflexive("projectiles", mulg_runtime_multiplayer_constant_projectile),
    h3_reflexive("equipment", mulg_runtime_multiplayer_constant_equipment),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=40, VISIBLE=False),
    Float("maximum_random_spawn_bias"),
    Float("teleporter_recharge_time"),
    Float("grenade_danger_weight"),
    Float("grenade_danger_inner_radius"),
    Float("grenade_danger_outer_radius"),
    Float("grenade_danger_lead_time"),
    Float("vehicle_danger_minimum_speed"),
    Float("vehicle_danger_weight"),
    Float("vehicle_danger_radius"),
    Float("vehicle_danger_lead_time"),
    Float("vehicle_nearby_player_distance"),
    h3_dependency("hill_shader"),
    Array("unknown_array_2", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    h3_dependency("bomb_explode_effect"),
    h3_dependency("unknown_0"),
    h3_dependency("bomb_explode_damage_effect"),
    h3_dependency("bomb_defuse_effect"),
    h3_dependency("cursor_impact_effect"),
    h3_string_id("bomb_defusal_string"),
    h3_string_id("blocked_teleporter_string"),
    h3_string_id("unknown_1", VISIBLE=False),
    h3_string_id("spawn_allowed_default_respawn_string"),
    h3_string_id("spawn_at_player_looking_at_self_string"),
    h3_string_id("spawn_at_player_looking_at_target_string"),
    h3_string_id("spawn_at_player_looking_at_potential_target_string"),
    h3_string_id("spawn_at_territory_allowed_looking_at_target_string"),
    h3_string_id("spawn_at_territory_allowed_looking_at_potential_target_string"),
    h3_string_id("player_out_of_lives_string"),
    h3_string_id("invalid_spawn_target_string"),
    h3_string_id("targetted_player_enemies_nearby_string"),
    h3_string_id("targetted_player_unfriendly_team_string"),
    h3_string_id("targetted_player_is_dead_string"),
    h3_string_id("targetted_player_in_combat_string"),
    h3_string_id("targetted_player_too_far_from_owned_flag_string"),
    h3_string_id("no_available_netpoints_string"),
    h3_string_id("netpoint_contested_string"),
    ENDIAN=">", SIZE=540
    )


mulg_runtime_state_response = Struct("state_response", 
    Bool16("flags", *unknown_flags_16),
    SInt16("unknown_0", VISIBLE=False),
    SEnum16("state", *mulg_runtime_state_response_state),
    SInt16("unknown_1", VISIBLE=False),
    h3_string_id("free_for_all_message"),
    h3_string_id("team_message"),
    h3_dependency("unknown_2"),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


mulg_runtime = Struct("runtime", 
    h3_dependency("sandbox_editor_unit"),
    h3_dependency("sandbox_editor_object"),
    h3_dependency("flag"),
    h3_dependency("ball"),
    h3_dependency("bomb"),
    h3_dependency("vip_zone"),
    h3_dependency("in_game_strings"),
    h3_reflexive("sounds", mulg_runtime_sound),
    h3_reflexive("looping_sounds", mulg_runtime_looping_sound),
    h3_reflexive("general_events", mulg_runtime_general_event),
    h3_reflexive("flavor_events", mulg_runtime_flavor_event),
    h3_reflexive("slayer_events", mulg_runtime_slayer_event),
    h3_reflexive("ctf_events", mulg_runtime_ctf_event),
    h3_reflexive("oddball_events", mulg_runtime_oddball_event),
    h3_reflexive("king_of_the_hill_events", mulg_runtime_king_of_the_hill_event),
    h3_reflexive("vip_events", mulg_runtime_vip_event),
    h3_reflexive("juggernaut_events", mulg_runtime_juggernaut_event),
    h3_reflexive("territories_events", mulg_runtime_territories_event),
    h3_reflexive("assault_events", mulg_runtime_assault_event),
    h3_reflexive("infection_events", mulg_runtime_infection_event),
    SInt32("default_frag_grenade_count"),
    SInt32("default_plasma_grenade_count"),
    h3_reflexive("multiplayer_constants", mulg_runtime_multiplayer_constant),
    h3_reflexive("state_responses", mulg_runtime_state_response),
    h3_dependency("scoreboard_emblem_bitmap"),
    h3_dependency("scoreboard_dead_emblem_bitmap"),
    h3_dependency("default_shape_shader"),
    h3_dependency("unknown"),
    h3_dependency("ctf_intro_ui"),
    h3_dependency("slayer_intro_ui"),
    h3_dependency("oddball_intro_ui"),
    h3_dependency("king_of_the_hill_intro_ui"),
    h3_dependency("sandbox_intro_ui"),
    h3_dependency("vip_intro_ui"),
    h3_dependency("juggernaut_intro_ui"),
    h3_dependency("territories_intro_ui"),
    h3_dependency("assault_intro_ui"),
    h3_dependency("infection_intro_ui"),
    ENDIAN=">", SIZE=524
    )


mulg_body = Struct("tagdata", 
    h3_reflexive("universal", mulg_universal),
    h3_reflexive("runtime", mulg_runtime),
    ENDIAN=">", SIZE=24
    )


def get():
    return mulg_def

mulg_def = TagDef("mulg",
    h3_blam_header('mulg'),
    mulg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["mulg"], endian=">", tag_cls=H3Tag
    )