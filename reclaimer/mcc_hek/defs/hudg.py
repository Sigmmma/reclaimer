#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

button_icon = Struct("button_icon",
    SInt16("sequence_index"),
    SInt16("width_offset"),
    QStruct("offset_from_reference_corner",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    #QStruct("override_icon_color", INCLUDE=argb_byte),
    UInt32("override_icon_color", INCLUDE=argb_uint32),
    SInt8("frame_rate", MIN=0, MAX=30, UNIT_SCALE=per_sec_unit_scale),
    Bool8("flags",
        "use_text_from_string_list_instead",
        "override_default_color",
        "width_offset_is_absolute_icon_width",
        ),
    SInt16("text_index"),
    SIZE=16
    )

waypoint_arrow = Struct("waypoint_arrow",
    ascii_str32("name"),

    Pad(8),
    #QStruct("color", INCLUDE=xrgb_byte),
    UInt32("color", INCLUDE=xrgb_uint32),
    Float("opacity"),
    Float("translucency"),
    SInt16("on_screen_sequence_index"),
    SInt16("off_screen_sequence_index"),
    SInt16("occluded_sequence_index"),

    Pad(18),
    Bool32("flags",
        "dont_rotate_when_pointing_offscreen"
        ),
    SIZE=104
    )


messaging_parameters = Struct("messaging_parameters",
    SEnum16("anchor", *hud_anchors),

    Pad(34),
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
    dependency("single_player_font", "font"),
    dependency("multi_player_font", "font"),
    float_sec("up_time"),
    float_sec("fade_time"),
    QStruct("icon_color", INCLUDE=argb_float),
    QStruct("text_color", INCLUDE=argb_float),
    Float("text_spacing"),
    dependency("item_message_text", "ustr"),
    dependency("icon_bitmap", "bitm"),
    dependency("alternate_icon_text", "ustr"),
    SIZE=196
    )

hud_help_text_color = Struct("hud_help_text_color",
    #QStruct("default_color", INCLUDE=argb_byte),
    #QStruct("flashing_color", INCLUDE=argb_byte),
    UInt32("default_color", INCLUDE=argb_uint32),
    UInt32("flashing_color", INCLUDE=argb_uint32),
    float_sec("flash_period"),
    float_sec("flash_delay"),
    SInt16("number_of_flashes"),
    Bool16("flash_flags", *hud_flash_flags),
    float_sec("flash_length"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    SIZE=32
    )

objective_colors = Struct("objective_colors",
    #QStruct("default_color", INCLUDE=argb_byte),
    #QStruct("flashing_color", INCLUDE=argb_byte),
    UInt32("default_color", INCLUDE=argb_uint32),
    UInt32("flashing_color", INCLUDE=argb_uint32),
    float_sec("flash_period"),
    float_sec("flash_delay"),
    SInt16("number_of_flashes"),
    Bool16("flash_flags", *hud_flash_flags),
    float_sec("flash_length"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    SInt16("uptime_ticks", UNIT_SCALE=sec_unit_scale),
    SInt16("fade_ticks", UNIT_SCALE=sec_unit_scale),
    SIZE=32
    )

waypoint_parameters = Struct("waypoint_parameters",
    Float("top_offset"),
    Float("bottom_offset"),
    Float("left_offset"),
    Float("right_offset"),

    Pad(32),
    dependency("arrow_bitmaps", "bitm"),
    SIZE=64
    )

hud_globals = Struct("hud_globals",
    Float("hud_scale_in_multiplayer"),

    Pad(256),
    dependency("default_weapon_hud", "wphi"),
    Float("motion_sensor_range"),
    Float("motion_sensor_velocity_sensitivity"),
    Float("motion_sensor_scale", DEFAULT=32.0),  # DONT TOUCH(why?)
    QStruct("default_chapter_title_bounds",
        SInt16("t"), SInt16("l"), SInt16("b"), SInt16("r"), ORIENT='h'
        ),
    SIZE=340
    )

hud_damage_indicators = Struct("hud_damage_indicators",
    SInt16("top_offset"),
    SInt16("bottom_offset"),
    SInt16("left_offset"),
    SInt16("right_offset"),

    Pad(32),
    dependency("indicator_bitmap", "bitm"),
    SInt16("sequence_index"),
    SInt16("multiplayer_sequence_index"),
    #QStruct("color", INCLUDE=argb_byte),
    UInt32("color", INCLUDE=argb_uint32),
    SIZE=80
    )

time_running_out = Struct("time_running_out_flash_color",
    #QStruct("default_color", INCLUDE=argb_byte),
    #QStruct("flashing_color", INCLUDE=argb_byte),
    UInt32("default_color", INCLUDE=argb_uint32),
    UInt32("flashing_color", INCLUDE=argb_uint32),
    float_sec("flash_period"),
    float_sec("flash_delay"),
    SInt16("number_of_flashes"),
    Bool16("flash_flags", *hud_flash_flags),
    float_sec("flash_length"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    SIZE=32
    )

time_out = Struct("time_out_flash_color",
    #QStruct("default_color", INCLUDE=argb_byte),
    #QStruct("flashing_color", INCLUDE=argb_byte),
    UInt32("default_color", INCLUDE=argb_uint32),
    UInt32("flashing_color", INCLUDE=argb_uint32),
    float_sec("flash_period"),
    float_sec("flash_delay"),
    SInt16("number_of_flashes"),
    Bool16("flash_flags", *hud_flash_flags),
    float_sec("flash_length"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    SIZE=32
    )

misc_hud_crap = Struct("misc_hud_crap",
    SInt16("loading_begin_text"),
    SInt16("loading_end_text"),
    SInt16("checkpoint_begin_text"),
    SInt16("checkpoint_end_text"),
    dependency("checkpoint", "snd!"),
    BytearrayRaw("unknown", SIZE=96, VISIBLE=False),
    SIZE=120
    )

hudg_body = Struct("tagdata",
    messaging_parameters,
    reflexive("button_icons", button_icon, 18,
        "a button", "b button", "x button", "y button",
        "black button", "white button", "left trigger", "right trigger",
        "dpad up",  "dpad down", "dpad left", "dpad right", "start", "back",
        "left thumb button", "right thumb button", "left stick", "right stick"
        ),
    hud_help_text_color,
    dependency("hud_messages", "hmt "),
    objective_colors,
    waypoint_parameters,
    reflexive("waypoint_arrows", waypoint_arrow, 16, DYN_NAME_PATH='.name'),

    Pad(80),
    hud_globals,
    hud_damage_indicators,
    time_running_out,
    time_out,

    Pad(40),
    dependency("carnage_report_bitmap", "bitm"),
    misc_hud_crap,
    SIZE=1104
    )


def get():
    return hudg_def

hudg_def = TagDef("hudg",
    blam_header("hudg"),
    hudg_body,

    ext=".hud_globals", endian=">", tag_cls=HekTag,
    )
