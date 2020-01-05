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

velocity_properties = Struct("velocity_properties",
    SEnum16("attachment", *function_outputs),
    Pad(2),
    Float("velocity", UNIT_SCALE=per_sec_unit_scale),
    Float("low_multiplier"),
    Float("high_multiplier")
    )

glw__body = Struct("tagdata",
    ascii_str32("attachment_marker"),
    SInt16("number_of_particles"),
    SEnum16("boundary_effect",
        "bounce",
        "wrap",
        ),
    SEnum16("normal_particle_distribution",
        "random",
        "uniform",
        ),
    SEnum16("trailing_particle_distribution",
        "vertically",
        "normal",
        "randomly"
        ),
    Bool32("glow_flags" ,
        "modify_particle_color_in_range",
        "particles_move_backwards",
        "particles_move_in_both_directions",
        "trailing_particles_fade_over_time",
        "trailing_particles_shrink_over_time",
        "trailing_particles_slow_over_time",
        ),

    Pad(36),
    Struct("particle_rotational_velocity", INCLUDE=velocity_properties),
    Struct("effect_rotational_velocity", INCLUDE=velocity_properties),
    Struct("effect_translational_velocity", INCLUDE=velocity_properties),
    Struct("particle_distance_to_object",
        SEnum16("attachment", *function_outputs),
        Pad(2),
        Float("min_distance"),
        Float("max_distance"),
        Float("low_multiplier"),
        Float("high_multiplier")
        ),

    Pad(8),
    Struct("particle_size",
        SEnum16("attachment", *function_outputs),
        Pad(2),
        from_to_wu("size_bounds"),  # world units
        QStruct("size_attachment_multiplier", INCLUDE=from_to),
        ),

    Struct("particle_color",
        SEnum16("attachment", *function_outputs),
        Pad(2),
        QStruct("lower_bound", INCLUDE=argb_float),
        QStruct("upper_bound", INCLUDE=argb_float),
        QStruct("lower_scale", INCLUDE=argb_float),
        QStruct("upper_scale", INCLUDE=argb_float)
        ),

    Float("color_rate_of_change"),
    Float("fading_percentage_of_glow"),
    Float("particle_generation_frequency",
           SIDETIP="Hz", UNIT_SCALE=per_sec_unit_scale),
    float_sec("lifetime_of_trailing_particles"),
    float_wu_sec("velocity_of_trailing_particles"),
    float_sec("trailing_particle_min_time"),
    float_sec("trailing_particle_max_time"),

    Pad(52),
    dependency("texture",  "bitm"),
    SIZE=340,
    )

def get():
    return glw__def

glw__def = TagDef("glw!",
    blam_header('glw!'),
    glw__body,

    ext=".glow", endian=">", tag_cls=HekTag
    )
