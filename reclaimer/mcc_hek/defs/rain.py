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

particle_type = Struct("particle_type",
    ascii_str32("name"),
    Bool32("flags",
        "blend_colors_in_hsv",
        "along_long_hue_path",
        "random_rotation",
        ),
    QStruct("fade",
        float_wu("in_start_distance"),
        float_wu("in_end_distance"),
        float_wu("out_start_distance"),
        float_wu("out_end_distance"),
        float_wu("in_start_height"),
        float_wu("in_end_height"),
        float_wu("out_start_height"),
        float_wu("out_end_height"),
        ),

    Pad(96),
    QStruct("particle_count", INCLUDE=from_to,
        SIDETIP="particles/(world unit^3)"),
    dependency("physics", "pphy"),

    Pad(16),
    Struct("acceleration",
        QStruct("magnitude", INCLUDE=from_to),
        float_rad("turning_rate"),  # radians
        Float("change_rate"),
        ),

    Pad(32),
    from_to_wu("particle_radius"),
    QStruct("animation_rate",
        Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
        Float("to",   UNIT_SCALE=per_sec_unit_scale),
        ORIENT='h', SIDETIP="frames/sec"
        ),
    from_to_rad_sec("rotation_rate"),  # radians/sec

    Pad(32),
    QStruct("color_lower_bound", INCLUDE=argb_float),
    QStruct("color_upper_bound", INCLUDE=argb_float),

    #Shader
    Struct("shader",
        Pad(64),
        dependency("sprite_bitmap", "bitm"),
        SEnum16("render_mode", *render_mode),
        SEnum16("render_direction_source",
            "from_velocity",
            "from_acceleration"
            ),

        Pad(40),
        Bool16("shader_flags", *shader_flags),
        SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
        SEnum16("framebuffer_fade_mode", *render_fade_mode),
        Bool16("map_flags",
            "unfiltered"
            )
        ),

    #Secondary bitmap
    Struct("secondary_bitmap",
        Pad(28),
        dependency("bitmap", "bitm"),
        SEnum16("anchor", *render_anchor),
        Bool16("secondary_map_flags",
            "unfiltered"
            ),
        Struct("u_animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v_animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation_animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation_center", INCLUDE=xy_float)
        ),

    Pad(4),
    Float("zsprite_radius_scale"),

    SIZE=604
    )

rain_body = Struct("tagdata",
    Pad(36),
    reflexive("particle_types", particle_type, 8, DYN_NAME_PATH='.name'),

    SIZE=48,
    )


def get():
    return rain_def

rain_def = TagDef("rain",
    blam_header("rain"),
    rain_body,

    ext=".weather_particle_system", endian=">", tag_cls=HekTag,
    )
