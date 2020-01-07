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
from .grhi import hud_background

warning_sound = Struct("warning_sound",
    dependency("sound", ('lsnd', 'snd!')),
    Bool32("latched_to",
        "shield_recharging",
        "shield_recharged",
        "shield_low",
        "shield_empty",
        "health_low",
        "health_empty",
        "health_minor_damage",
        "health_major_damage",
        ),
    Float("scale"),
    SIZE=56
    )

shield_panel_meter = Struct("shield_panel_meter",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter_bitmap", "bitm"),
    #QStruct("color_at_meter_minimum", INCLUDE=xrgb_byte),
    #QStruct("color_at_meter_maximum", INCLUDE=xrgb_byte),
    #QStruct("flash_color", INCLUDE=xrgb_byte),
    #QStruct("empty_color", INCLUDE=argb_byte),
    UInt32("color_at_meter_minimum", INCLUDE=xrgb_uint32),
    UInt32("color_at_meter_maximum", INCLUDE=xrgb_uint32),
    UInt32("flash_color", INCLUDE=xrgb_uint32),
    UInt32("empty_color", INCLUDE=argb_uint32),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum_meter_value"),
    SInt16("sequence_index"),
    SInt8("alpha_multiplier"),
    SInt8("alpha_bias"),
    SInt16("value_scale"),
    Float("opacity"),
    Float("translucency"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    Pad(16),
    #QStruct("overcharge_minimum_color", INCLUDE=xrgb_byte),
    #QStruct("overcharge_maximum_color", INCLUDE=xrgb_byte),
    #QStruct("overcharge_flash_color", INCLUDE=xrgb_byte),
    #QStruct("overcharge_empty_color", INCLUDE=xrgb_byte),
    UInt32("overcharge_minimum_color", INCLUDE=xrgb_uint32),
    UInt32("overcharge_maximum_color", INCLUDE=xrgb_uint32),
    UInt32("overcharge_flash_color", INCLUDE=xrgb_uint32),
    UInt32("overcharge_empty_color", INCLUDE=xrgb_uint32),
    SIZE=136
    )

health_panel_meter = Struct("health_panel_meter",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter_bitmap", "bitm"),
    #QStruct("color_at_meter_minimum", INCLUDE=xrgb_byte),
    #QStruct("color_at_meter_maximum", INCLUDE=xrgb_byte),
    #QStruct("flash_color", INCLUDE=xrgb_byte),
    #QStruct("empty_color", INCLUDE=argb_byte),
    UInt32("color_at_meter_minimum", INCLUDE=xrgb_uint32),
    UInt32("color_at_meter_maximum", INCLUDE=xrgb_uint32),
    UInt32("flash_color", INCLUDE=xrgb_uint32),
    UInt32("empty_color", INCLUDE=argb_uint32),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum_meter_value"),
    SInt16("sequence_index"),
    SInt8("alpha_multiplier"),
    SInt8("alpha_bias"),
    SInt16("value_scale"),
    Float("opacity"),
    Float("translucency"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    Pad(16),
    #QStruct("medium_health_left_color", INCLUDE=xrgb_byte),
    UInt32("medium_health_left_color", INCLUDE=xrgb_uint32),
    Float("max_color_health_fraction_cutoff"),
    Float("min_color_health_fraction_cutoff"),
    SIZE=136
    )

motion_sensor_center = Struct("motion_sensor_center",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),
    SIZE=16
    )

auxilary_overlay = Struct("auxilary_overlay",
    Struct("background", INCLUDE=hud_background),
    SEnum16("type",
        "team_icon"
        ),
    Bool16("flags",
        "use_team_color"
        ),
    SIZE=132
    )

auxilary_meter = Struct("auxilary_meter",
    Pad(18),
    SEnum16("type", "integrated_light", VISIBLE=False),
    Struct("background", INCLUDE=hud_background),

    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter_bitmap", "bitm"),
    #QStruct("color_at_meter_minimum", INCLUDE=xrgb_byte),
    #QStruct("color_at_meter_maximum", INCLUDE=xrgb_byte),
    #QStruct("flash_color", INCLUDE=xrgb_byte),
    #QStruct("empty_color", INCLUDE=argb_byte),
    UInt32("color_at_meter_minimum", INCLUDE=xrgb_uint32),
    UInt32("color_at_meter_maximum", INCLUDE=xrgb_uint32),
    UInt32("flash_color", INCLUDE=xrgb_uint32),
    UInt32("empty_color", INCLUDE=argb_uint32),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum_meter_value"),
    SInt16("sequence_index"),
    SInt8("alpha_multiplier"),
    SInt8("alpha_bias"),
    SInt16("value_scale"),
    Float("opacity"),
    Float("translucency"),
    #QStruct("disabled_color", INCLUDE=argb_byte),
    UInt32("disabled_color", INCLUDE=argb_uint32),

    Pad(16),
    Float("minimum_fraction_cutoff"),
    Bool32("overlay_flags",
        "show_only_when_active",
        "flash_once_if_activated_while_disabled",
        ),

    SIZE=324,
    COMMENT="\nThis auxilary meter is meant for the flashlight.\n"
    )

unhi_body = Struct("tagdata",
    SEnum16("anchor", *hud_anchors),

    Pad(34),
    Struct("unit_hud_background", INCLUDE=hud_background),
    Struct("shield_panel_background", INCLUDE=hud_background),
    shield_panel_meter,
    Struct("health_panel_background", INCLUDE=hud_background),
    health_panel_meter,
    Struct("motion_sensor_background", INCLUDE=hud_background),
    Struct("motion_sensor_foreground", INCLUDE=hud_background),

    Pad(32),
    motion_sensor_center,

    Pad(20),
    SEnum16("auxilary_overlay_anchor", *hud_anchors),
    Pad(34),
    reflexive("auxilary_overlays", auxilary_overlay, 16),

    Pad(16),
    reflexive("warning_sounds", warning_sound, 12,
        DYN_NAME_PATH='.sound.filepath'),
    reflexive("auxilary_meters", auxilary_meter, 16),

    SIZE=1388
    )


def get():
    return unhi_def

unhi_def = TagDef("unhi",
    blam_header("unhi"),
    unhi_body,

    ext=".unit_hud_interface", endian=">", tag_cls=HekTag,
    )
