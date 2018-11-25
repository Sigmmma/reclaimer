from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

wigl_alert_icon = (
    "none",
    "download",
    "pause",
    "upload",
    "checkbox",
    )

wigl_dialog_default_option = (
    "option_1",
    "option_2",
    "option_3",
    "option_4",
    )


wigl_text_color = Struct("text_colors",
    string_id_meta("name"),
    color_argb_float("color"),
    ENDIAN=">", SIZE=20
    )


wigl_player_color_player_text_color = Struct("player_text_color",
    color_argb_float("color"),
    ENDIAN=">", SIZE=16
    )


wigl_player_color_team_text_color = Struct("team_text_color",
    color_argb_float("color"),
    ENDIAN=">", SIZE=16
    )


wigl_player_color_player_ui_color = Struct("player_ui_color",
    color_argb_float("color"),
    ENDIAN=">", SIZE=16
    )


wigl_player_color_team_ui_color = Struct("team_ui_color",
    color_argb_float("color"),
    ENDIAN=">", SIZE=16
    )


wigl_player_color = Struct("player_colors",
    reflexive("player_text_color", wigl_player_color_player_text_color),
    reflexive("team_text_color", wigl_player_color_team_text_color),
    reflexive("player_ui_color", wigl_player_color_player_ui_color),
    reflexive("team_ui_color", wigl_player_color_team_ui_color),
    ENDIAN=">", SIZE=48
    )


wigl_alert = Struct("alerts",
    string_id_meta("name"),
    Bool8("flags",
        ),
    SInt8("unknown"),
    SEnum8("icon", *wigl_alert_icon),
    SInt8("unknown_1"),
    string_id_meta("title"),
    string_id_meta("body"),
    ENDIAN=">", SIZE=16
    )


wigl_dialog = Struct("dialogs",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    string_id_meta("title"),
    string_id_meta("body"),
    string_id_meta("option_1"),
    string_id_meta("option_2"),
    string_id_meta("option_3"),
    string_id_meta("option_4"),
    string_id_meta("key_legend"),
    SEnum16("default_option", *wigl_dialog_default_option),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=40
    )


wigl_global_data_source = Struct("global_data_sources",
    dependency("data_source"),
    ENDIAN=">", SIZE=16
    )


wigl_meta_def = BlockDef("wigl",
    SInt16("inc_text_update_period"),
    SInt16("inc_text_block_character"),
    Float("near_clip_plane_distance"),
    Float("projection_plane_distance"),
    Float("far_clip_plane_distance"),
    dependency("global_strings"),
    dependency("damage_type_strings"),
    dependency("main_menu_music"),
    SInt32("music_fade_time"),
    color_argb_float("color"),
    color_argb_float("text_stroke_color"),
    reflexive("text_colors", wigl_text_color),
    reflexive("player_colors", wigl_player_color),
    dependency("ui_sounds"),
    reflexive("alerts", wigl_alert),
    reflexive("dialogs", wigl_dialog),
    reflexive("global_data_sources", wigl_global_data_source),
    Float("widescreen_bitmap_scale_x"),
    Float("widescreen_bitmap_scale_y"),
    Float("standard_bitmap_scale_x"),
    Float("standard_bitmap_scale_y"),
    Float("menu_blur_x"),
    Float("menu_blur_y"),
    StrLatin1("ui_spartan_biped_name", SIZE=32),
    StrLatin1("ui_spartan_ai_squad_name", SIZE=32),
    string_id_meta("ui_spartan_ai_location_name"),
    StrLatin1("ui_elite_biped_name", SIZE=32),
    StrLatin1("ui_elite_ai_squad_name", SIZE=32),
    string_id_meta("ui_elite_ai_location_name"),
    SInt32("single_scroll_speed"),
    SInt32("scroll_speed_transition_wait_time"),
    SInt32("held_scroll_speed"),
    SInt32("attract_video_idle_wait"),
    TYPE=Struct, ENDIAN=">", SIZE=352
    )