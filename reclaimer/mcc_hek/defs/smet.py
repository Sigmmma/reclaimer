#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .shdr import *
from .objs.shdr import ShdrTag
from supyr_struct.defs.tag_def import TagDef

smet_attrs = Struct("smet_attrs",
    #Meter Shader Properties
    Struct("meter_shader",
        Bool16("meter_shader_flags",
            "decal",
            "two_sided",
            "flash_color_is_negative",
            "tint_mode_2",
            "unfiltered"
            ),
        Pad(34),
        dependency("map", "bitm"),
        Pad(32),
        ),

    #Colors
    Struct("colors",
        Struct("gadient_min", INCLUDE=rgb_float),
        Struct("gadient_max", INCLUDE=rgb_float),
        Struct("background", INCLUDE=rgb_float),
        Struct("flash", INCLUDE=rgb_float),
        Struct("tint", INCLUDE=rgb_float),
        float_zero_to_one("meter_transparency"),
        float_zero_to_one("background_transparency"),
        ),

    Pad(24),
    #External Function Sources
    Struct("external_function_sources",
        SEnum16("meter_brightness", *function_outputs),
        SEnum16("flash_brightness", *function_outputs),
        SEnum16("value",            *function_outputs),
        SEnum16("gradient",         *function_outputs),
        SEnum16("flash_extension",  *function_outputs),
        ),
    SIZE=220,
    )

smet_body = Struct("tagdata",
    shdr_attrs,
    smet_attrs,
    SIZE=260,
    )



def get():
    return smet_def

smet_def = TagDef("smet",
    blam_header('smet'),
    smet_body,

    ext=".shader_transparent_meter", endian=">", tag_cls=ShdrTag
    )
