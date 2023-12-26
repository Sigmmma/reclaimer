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

sgla_attrs = Struct("sgla_attrs",
    #Glass Shader Properties
    Bool16("glass_shader_flags",
        "alpha_tested",
        "decal",
        "two_sided",
        "bump_map_is_specular_mask",
        ),

    Pad(42),
    #Background Tint Properties
    Struct("background_tint_properties",
        QStruct("color", INCLUDE=rgb_float),
        Float("map_scale"),
        dependency("map", "bitm"),
        ),

    Pad(22),
    #Reflection Properties
    Struct("reflection_properties",
        SEnum16("type",
            "bumped_cubemap",
            "flat_cubemap",
            "dynamic_mirror",
            ),
        float_zero_to_one("perpendicular_brightness"),  # [0,1]
        QStruct("perpendicular_tint_color", INCLUDE=rgb_float),
        float_zero_to_one("parallel_brightness"),  # [0,1]
        QStruct("parallel_tint_color", INCLUDE=rgb_float),
        dependency("map", "bitm"),

        Float("bump_map_scale"),
        dependency("bump_map", "bitm"),
        ),

    Pad(132),
    #Diffuse Properties
    Struct("diffuse_properties",
        Float("map_scale"),
        dependency("map", "bitm"),
        Float("detail_map_scale"),
        dependency("detail_map", "bitm"),
        ),

    Pad(32),
    #Specular Properties
    Struct("specular_properties",
        Float("map_scale"),
        dependency("map", "bitm"),
        Float("detail_map_scale"),
        dependency("detail_map", "bitm"),
        ),
    SIZE=440
    )

sgla_body = Struct("tagdata",
    shdr_attrs,
    sgla_attrs,
    SIZE=480,
    )


def get():
    return sgla_def

sgla_def = TagDef("sgla",
    blam_header('sgla'),
    sgla_body,

    ext=".shader_transparent_glass", endian=">", tag_cls=ShdrTag
    )
