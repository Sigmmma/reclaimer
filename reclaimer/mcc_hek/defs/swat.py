#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import pi

from .shdr import *
from .objs.shdr import ShdrTag
from supyr_struct.defs.tag_def import TagDef

ripple = Struct("ripple",
    Pad(4),
    float_zero_to_one("contribution_factor"),
    Pad(32),
    Float("animation_angle",
        MIN=0.0, MAX=2*pi, UNIT_SCALE=180/pi, SIDETIP="[0,360]"),  # radians
    Float("animation_velocity", UNIT_SCALE=per_sec_unit_scale),
    Struct("map_offset", INCLUDE=ij_float),
    UInt16("map_repeats"),
    UInt16("map_index"),
    SIZE=76
    )


swat_attrs = Struct("swat_attrs",
    #Water Shader Properties
    Struct("water_shader",
        Bool16("flags",
            "base_map_alpha_modulates_reflection",
            "base_map_color_modulates_background",
            "atmospheric_fog",
            "draw_before_fog",
            ),
        Pad(34),
        dependency("base_map", "bitm"),
        Pad(16),
        float_zero_to_one("perpendicular_brightness"),
        Struct("perpendicular_tint_color", INCLUDE=rgb_float),
        float_zero_to_one("parallel_brightness"),
        Struct("parallel_tint_color", INCLUDE=rgb_float),
        Pad(16),
        dependency("reflection_map", "bitm"),

        Pad(16),
        Float("ripple_animation_angle",
            MIN=0.0, MAX=2*pi, UNIT_SCALE=180/pi, SIDETIP="[0,360]"),  # radians
        Float("ripple_animation_velocity", UNIT_SCALE=per_sec_unit_scale),
        Float("ripple_scale"),
        dependency("ripple_maps", "bitm"),
        UInt16("ripple_mipmap_levels"),
        Pad(2),
        float_zero_to_one("ripple_mipmap_fade_factor"),
        Float("ripple_mipmap_detail_bias"),
        ),

    Pad(64),
    reflexive("ripples", ripple, 4),
    SIZE=280
    )

swat_body = Struct("tagdata",
    shdr_attrs,
    swat_attrs,
    SIZE=320,
    )

def get():
    return swat_def

swat_def = TagDef("swat",
    blam_header('swat', 2),
    swat_body,

    ext=".shader_transparent_water", endian=">", tag_cls=ShdrTag
    )
