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

messaging_information = Struct("messaging_information",
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
    SIZE=64
    )

effector = Struct("effector",
    Pad(64),
    SEnum16("destination_type",
        "tint_0_to_1",
        "horizontal_offset",
        "vertical_offset",
        "fade_0_to_1",
        ),
    SEnum16("destination",
        "geometry_offset",
        "primary_map",
        "secondary_map",
        "tertiary_map",
        ),
    SEnum16("source",
        "player_pitch",
        "player_tangent",
        "player_yaw",
        "weapon_total_ammo",
        "weapon_loaded_ammo",
        "weapon_heat",
        "explicit",  # use low bound
        "weapon_zoom_level",
        ),

    Pad(2),
    QStruct("in_bounds", INCLUDE=from_to,
        SIDETIP="source_units"),  # source units
    QStruct("out_bounds", INCLUDE=from_to, SIDETIP="pixels"),  # pixels

    Pad(64),
    QStruct("tint_color_lower_bound", INCLUDE=rgb_float),
    QStruct("tint_color_upper_bound", INCLUDE=rgb_float),
    Struct("periodic_functions", INCLUDE=anim_func_per_pha),
    SIZE=220
    )

multitex_overlay = Struct("multitex_overlay",
    Pad(2),
    SInt16("type"),
    SEnum16("framebuffer_blend_func", *framebuffer_blend_functions),

    # Anchors
    Pad(34),
    SEnum16("primary_anchor", *multitex_anchors),
    SEnum16("secondary_anchor", *multitex_anchors),
    SEnum16("tertiary_anchor", *multitex_anchors),
    # Blending function
    SEnum16("zero_to_one_blend_func", *blending_funcs),
    SEnum16("one_to_two_blend_func", *blending_funcs),

    # Map scales
    Pad(2),
    QStruct("primary_scale", INCLUDE=xy_float),
    QStruct("secondary_scale", INCLUDE=xy_float),
    QStruct("tertiary_scale", INCLUDE=xy_float),
    # Map offsets
    QStruct("primary_offset", INCLUDE=xy_float),
    QStruct("secondary_offset", INCLUDE=xy_float),
    QStruct("tertiary_offset", INCLUDE=xy_float),

    # Maps
    dependency("primary_map", "bitm"),
    dependency("secondary_map", "bitm"),
    dependency("tertiary_map", "bitm"),
    SEnum16("primary_wrap_mode", *multitex_wrap_modes),
    SEnum16("secondary_wrap_mode", *multitex_wrap_modes),
    SEnum16("tertiary_wrap_mode", *multitex_wrap_modes),

    Pad(186),
    reflexive("effectors", effector, 30),
    SIZE=480,
    )

total_grenades_numbers = Struct("total_grenades_numbers",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
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

    Pad(4),
    SInt8("maximum_number_of_digits"),
    Bool8("flags",
        "show_leading_zeros",
        "only_show_when_zoomed",
        "draw_a_trailing_m",
        ),
    SInt8("number_of_fractional_digits"),

    Pad(13),
    SInt16("flash_cutoff"),
    SIZE=88
    )

overlay = Struct("overlay",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
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

    Pad(4),
    float_sec("frame_rate"),
    SInt16("sequence_index"),
    Bool16("type",
        "show_on_flashing",
        "show_on_empty",
        "show_on_default",
        "show_always",
        ),
    Bool32("flags",
        "flashes_when_active",
        ),

    SIZE=136
    )

warning_sound = Struct("warning_sound",
    dependency("sound", ('lsnd', 'snd!')),
    Bool32("latched_to",
        "low_grenade_sound",
        "no_grenades_left",
        "throw_on_no_grenades",
        ),
    Float("scale"),
    SIZE=56
    )

# Use this with INCLUDE keywords since it will need to be named
hud_background = Struct("",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),

    Pad(22),
    dependency("interface_bitmap", "bitm"),
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

    Pad(4),
    SInt16("sequence_index"),

    Pad(2),
    reflexive("multitex_overlays", multitex_overlay, 30),
    Pad(4),
    SIZE=104
    )

grhi_body = Struct("tagdata",
    SEnum16("anchor", *hud_anchors),

    Pad(34),
    Struct("grenade_hud_background", INCLUDE=hud_background),
    Struct("total_grenades",
        Struct("background", INCLUDE=hud_background),
        Struct("numbers", INCLUDE=total_grenades_numbers),
        dependency("overlay_bitmap", "bitm"),
        reflexive("overlays", overlay, 16),
        ),
    reflexive("warning_sounds", warning_sound, 12,
        DYN_NAME_PATH='.sound.filepath'),

    Pad(68),
    messaging_information,
    SIZE=504,
    )


def get():
    return grhi_def

grhi_def = TagDef("grhi",
    blam_header("grhi"),
    grhi_body,

    ext=".grenade_hud_interface", endian=">", tag_cls=HekTag,
    )
