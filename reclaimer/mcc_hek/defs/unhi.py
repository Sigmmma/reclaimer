#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.unhi import *
from .grhi import hud_background, mcc_hud_anchor

# to reduce a lot of code, these have been snipped out
meter_xform_common = ( # NOTE: used by wphi
    QStruct("anchor_offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width_scale"),
    Float("height_scale"),
    Bool16("scaling_flags", *hud_scaling_flags),
    Pad(22),
    )
meter_common = ( # NOTE: used by wphi
    dependency("meter_bitmap", "bitm"),
    UInt32("color_at_meter_minimum", INCLUDE=xrgb_uint32),
    UInt32("color_at_meter_maximum", INCLUDE=xrgb_uint32),
    UInt32("flash_color", INCLUDE=xrgb_uint32),
    UInt32("empty_color", INCLUDE=argb_uint32),
    Bool8("flags",
        "use_min_max_for_state_changes",
        "interpolate_between_min_max_flash_colors_as_state_changes",
        "interpolate_color_along_hsv_space",
        "more_colors_for_hsv_interpolation",
        "invert_interpolation",
        "use_xbox_shading",
        ),
    SInt8("minimum_meter_value"),
    SInt16("sequence_index"),
    SInt8("alpha_multiplier"),
    SInt8("alpha_bias"),
    SInt16("value_scale"),
    Float("opacity"),
    Float("translucency"),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    )

shield_panel_meter = Struct("shield_panel_meter",
    *meter_xform_common,
    *meter_common,
    Float("min_alpha"),
    Pad(12),
    UInt32("overcharge_minimum_color", INCLUDE=xrgb_uint32),
    UInt32("overcharge_maximum_color", INCLUDE=xrgb_uint32),
    UInt32("overcharge_flash_color", INCLUDE=xrgb_uint32),
    UInt32("overcharge_empty_color", INCLUDE=xrgb_uint32),
    Pad(16),
    SIZE=136
    )

health_panel_meter = Struct("health_panel_meter",
    *meter_xform_common,
    *meter_common,
    Float("min_alpha"),
    Pad(12),
    UInt32("medium_health_left_color", INCLUDE=xrgb_uint32),
    Float("max_color_health_fraction_cutoff"),
    Float("min_color_health_fraction_cutoff"),
    Pad(20),
    SIZE=136
    )

auxilary_meter = Struct("auxilary_meter",
    Pad(18),
    SEnum16("type", "integrated_light", VISIBLE=False),
    Struct("background", INCLUDE=hud_background),

    *meter_xform_common,
    *meter_common,
    Float("min_alpha"),
    Pad(12),
    Float("minimum_fraction_cutoff"),
    Bool32("overlay_flags",
        "show_only_when_active",
        "flash_once_if_activated_while_disabled",
        ),
    Pad(24),
    Pad(64),

    SIZE=324,
    COMMENT="\nThis auxilary meter is meant for the flashlight.\n"
    )

unhi_body = desc_variant(unhi_body,
    SEnum16("anchor", *hud_anchors_mcc),
    shield_panel_meter,
    health_panel_meter,
    reflexive("auxilary_meters", auxilary_meter, 16),
    )

def get():
    return unhi_def

unhi_def = TagDef("unhi",
    blam_header("unhi"),
    unhi_body,

    ext=".unit_hud_interface", endian=">", tag_cls=HekTag,
    )
