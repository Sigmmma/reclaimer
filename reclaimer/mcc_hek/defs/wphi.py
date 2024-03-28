#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.wphi import *
from .grhi import multitex_overlay, mcc_hud_anchor
from .unhi import meter_xform_common, meter_common

# to reduce a lot of code, these have been snipped out
element_common = (
    attached_state,
    Pad(2),
    use_on_map_type,
    mcc_hud_anchor,
    Pad(28),
    )
element_flash_common = (
    UInt32("default_color", INCLUDE=argb_uint32),
    UInt32("flashing_color", INCLUDE=argb_uint32),
    float_sec("flash_period"),
    float_sec("flash_delay"),
    SInt16("number_of_flashes"),
    Bool16("flash_flags", *hud_flash_flags),
    float_sec("flash_length"),
    UInt32("disabled_color", INCLUDE=argb_uint32),
    )

static_element = Struct("static_element",
    *element_common,
    *meter_xform_common,
    dependency("interface_bitmap", "bitm"),
    *element_flash_common,

    Pad(4),
    SInt16("sequence_index"),

    Pad(2),
    reflexive("multitex_overlays", multitex_overlay, 30),
    SIZE=180
    )

meter_element = Struct("meter_element",
    *element_common,
    *meter_xform_common,
    *meter_common,
    SIZE=180
    )

number_element = Struct("number_element",
    *element_common,
    *meter_xform_common,
    *element_flash_common,

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

overlay_element = Struct("overlay_element",
    *element_common,
    dependency("overlay_bitmap", "bitm"),
    reflexive("overlays", overlay, 16),
    SIZE=104
    )

wphi_body = desc_variant(wphi_body,
    mcc_hud_anchor,
    reflexive("static_elements", static_element, 16),
    reflexive("meter_elements", meter_element, 16),
    reflexive("number_elements", number_element, 16),
    reflexive("overlay_elements", overlay_element, 16),
    )


def get():
    return wphi_def

wphi_def = TagDef("wphi",
    blam_header("wphi", 2),
    wphi_body,

    ext=".weapon_hud_interface", endian=">", tag_cls=WphiTag,
    )
