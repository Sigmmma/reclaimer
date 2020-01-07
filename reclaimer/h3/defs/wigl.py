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
# revision: 2		author: DarkShallFall
# 	Labeled about 40 values, structures, and idents.
# revision: 3		author: -DeToX- and DarkShallFall
# 	Labelled reflexives and found their purposes, aswell as the service tag bipd strings.
# revision: 4		author: Lord Zedd
# 	Got most things
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
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


wigl_text_color = Struct("text_color",
    h3_string_id("name"),
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


wigl_player_color = Struct("player_color",
    h3_reflexive("player_text_color", wigl_player_color_player_text_color),
    h3_reflexive("team_text_color", wigl_player_color_team_text_color),
    h3_reflexive("player_ui_color", wigl_player_color_player_ui_color),
    h3_reflexive("team_ui_color", wigl_player_color_team_ui_color),
    ENDIAN=">", SIZE=48
    )


wigl_alert = Struct("alert",
    h3_string_id("name"),
    Bool8("flags", *unknown_flags_8),
    SInt8("unknown_0"),
    SEnum8("icon", *wigl_alert_icon),
    SInt8("unknown_1", VISIBLE=False),
    h3_string_id("title"),
    h3_string_id("body"),
    ENDIAN=">", SIZE=16
    )


wigl_dialog = Struct("dialog",
    h3_string_id("name"),
    SInt16("unknown_0"),
    SInt16("unknown_1", VISIBLE=False),
    h3_string_id("title"),
    h3_string_id("body"),
    Array("option_array", SUB_STRUCT=h3_string_id("option"), SIZE=4),
    h3_string_id("key_legend"),
    SEnum16("default_option", *wigl_dialog_default_option),
    SInt16("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=40
    )


wigl_global_data_source = Struct("global_data_source",
    h3_dependency("data_source"),
    ENDIAN=">", SIZE=16
    )


wigl_body = Struct("tagdata",
    SInt16("inc_text_update_period"),
    SInt16("inc_text_block_character"),
    Float("near_clip_plane_distance"),
    Float("projection_plane_distance"),
    Float("far_clip_plane_distance"),
    h3_dependency("global_strings"),
    h3_dependency("damage_type_strings"),
    h3_dependency("main_menu_music"),
    SInt32("music_fade_time"),
    color_argb_float("color"),
    color_argb_float("text_stroke_color"),
    h3_reflexive("text_colors", wigl_text_color),
    h3_reflexive("player_colors", wigl_player_color),
    h3_dependency("ui_sounds"),
    h3_reflexive("alerts", wigl_alert),
    h3_reflexive("dialogs", wigl_dialog),
    h3_reflexive("global_data_sources", wigl_global_data_source),
    QStruct("widescreen_bitmap_scale", INCLUDE=xy_float),
    QStruct("standard_bitmap_scale", INCLUDE=xy_float),
    QStruct("menu_blur", INCLUDE=xy_float),
    ascii_str32("ui_spartan_biped_name"),
    ascii_str32("ui_spartan_ai_squad_name"),
    h3_string_id("ui_spartan_ai_location_name"),
    ascii_str32("ui_elite_biped_name"),
    ascii_str32("ui_elite_ai_squad_name"),
    h3_string_id("ui_elite_ai_location_name"),
    SInt32("single_scroll_speed"),
    SInt32("scroll_speed_transition_wait_time"),
    SInt32("held_scroll_speed"),
    SInt32("attract_video_idle_wait"),
    ENDIAN=">", SIZE=352
    )


def get():
    return wigl_def

wigl_def = TagDef("wigl",
    h3_blam_header('wigl'),
    wigl_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wigl"], endian=">", tag_cls=H3Tag
    )
