#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.wphi import WphiTag
from supyr_struct.defs.tag_def import TagDef
from .grhi import messaging_information, multitex_overlay, hud_background

crosshair_types = (
    "aim",
    "zoom",
    "charge",
    "should_reload",
    "flash_heat",
    "flash_total_ammo",
    "flash_battery",
    "reload_overheat",
    "flash_when_firing_and_no_ammo",
    "flash_when_throwing_grenade_and_no_grenade",
    "low_ammo_and_none_left_to_reload",
    "should_reload_secondary_trigger",
    "flash_secondary_total_ammo",
    "flash_secondary_reload",
    "flash_when_firing_secondary_and_no_ammo",
    "low_secondary_ammo_and_none_left_to_reload",
    "primary_trigger_ready",
    "secondary_trigger_ready",
    "flash_when_firing_with_depleted_battery",
    )

attached_state = SEnum16("state_attached_to",
    "total_ammo",
    "loaded_ammo",
    "heat",
    "age",
    "secondary_weapon_total_ammo",
    "secondary_weapon_loaded_ammo",
    "distance_to_target",
    "elevation_to_target",
    )

use_on_map_type = SEnum16("can_use_on_map_type",
    "any",
    "solo",
    "multiplayer",
    )

static_element = Struct("static_element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
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
    SIZE=180
    )

meter_element = Struct("meter_element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
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
    SIZE=180
    )

number_element = Struct("number_element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
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
    Pad(1),

    Pad(12),
    Bool16("weapon_specific_flags",
        "divide_number_by_magazine_size"
        ),
    SIZE=160
    )

crosshair_overlay = Struct("crosshair_overlay",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
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
    SInt16("frame_rate", UNIT_SCALE=per_sec_unit_scale),
    SInt16("sequence_index"),
    Bool32("type",
        "flashes_when_active",
        "not_a_sprite",
        "show_only_when_zoomed",
        "show_sniper_data",
        "hide_area_outside_reticle",
        "one_zoom_level",
        "dont_show_when_zoomed",
        ),
    SIZE=108
    )

overlay = Struct("overlay",
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
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
    SInt16("frame_rate", UNIT_SCALE=per_sec_unit_scale),
    Pad(2),
    SInt16("sequence_index"),
    Bool16("type",
        "show_on_flashing",
        "show_on_empty",
        "show_on_reload_overheating",
        "show_on_default",
        "show_always",
        ),
    Bool32("flags",
        "flashes_when_active",
        ),
    SIZE=136
    )

crosshair = Struct("crosshair",
    SEnum16("crosshair_type", *crosshair_types),
    Pad(2),
    use_on_map_type,

    Pad(30),
    dependency("crosshair_bitmap", "bitm"),
    reflexive("crosshair_overlays", crosshair_overlay, 16),
    SIZE=104
    )

overlay_element = Struct("overlay_element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    dependency("overlay_bitmap", "bitm"),
    reflexive("overlays", overlay, 16),
    SIZE=104
    )

screen_effect = Struct("screen_effect",
    Pad(4),
    Struct("mask",
        Bool16("flags",
            "only_when_zoomed"
            ),
        Pad(18),
        dependency("fullscreen_mask", "bitm"),
        dependency("splitscreen_mask", "bitm")
        ),

    Pad(8),
    Struct("convolution",
        Bool16("flags",
            "only_when_zoomed"
            ),
        Pad(2),
        from_to_rad("fov_in_bounds"),  # radians
        QStruct("radius_out_bounds",
            INCLUDE=from_to, SIDETIP="pixels")  # pixels
        ),

    Pad(24),
    Struct("night_vision",
        Bool16("flags",
            "only_when_zoomed",
            "connect_to_flashlight",
            "masked"
            ),
        SInt16("script_source", MIN=0, MAX=3, SIDETIP="[0,3]"),
        Float("intensity", MIN=0.0, MAX=1.0, SIDETIP="[0,1]")
        ),

    Pad(24),
    Struct("desaturation",
        Bool16("flags",
            "only_when_zoomed",
            "connect_to_flashlight",
            "additive",
            "masked"
            ),
        SInt16("script_source", MIN=0, MAX=3, SIDETIP="[0,3]"),
        Float("intensity", MIN=0.0, MAX=1.0, SIDETIP="[0,1]"),
        QStruct("tint", INCLUDE=rgb_float)
        ),
    SIZE=184
    )

wphi_body = Struct("tagdata",
    dependency("child_hud", "wphi"),
    Struct("flash_cutoffs",
        Bool16("flags",
            "use_parent_hud_flashing_parameters"
            ),
        Pad(2),
        SInt16("total_ammo_cutoff"),
        SInt16("loaded_ammo_cutoff"),
        SInt16("heat_cutoff"),
        SInt16("age_cutoff"),
        ),

    Pad(32),
    SEnum16("anchor", *hud_anchors),

    Pad(34),
    reflexive("static_elements", static_element, 16),
    reflexive("meter_elements", meter_element, 16),
    reflexive("number_elements", number_element, 16),
    reflexive("crosshairs", crosshair, 19),
    reflexive("overlay_elements", overlay_element, 16),
    FlBool32("crosshair_types", *crosshair_types, VISIBLE=False),

    # necessary for reticles to show up sometimes
    Pad(12),
    reflexive("screen_effect", screen_effect, 1),

    Pad(132),
    messaging_information,
    SIZE=380,
    )


def get():
    return wphi_def

wphi_def = TagDef("wphi",
    blam_header("wphi", 2),
    wphi_body,

    ext=".weapon_hud_interface", endian=">", tag_cls=WphiTag,
    )
