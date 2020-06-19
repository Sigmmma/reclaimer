#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.pctl import *
from supyr_struct.util import desc_variant


particle_state = Struct("particle_state",
    ascii_str32("name"),
    from_to_sec("duration_bounds"),
    from_to_sec("transition_time_bounds"),

    dependency("bitmaps", "bitm"),
    SInt16("sequence_index"),
    Pad(6),
    QStruct("scale", INCLUDE=from_to, SIDETIP="world units/pixel"),
    QStruct("animation_rate",
        Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
        Float("to",   UNIT_SCALE=per_sec_unit_scale),
        ORIENT='h', SIDETIP="frames/sec"
        ),
    from_to_rad_sec("rotation_rate"),  # radians/sec
    QStruct("color_1", INCLUDE=argb_float),
    QStruct("color_2", INCLUDE=argb_float),
    Float("radius_multiplier"),
    dependency("physics", "pphy"),

    Pad(72),
    FlUInt32("unknown0", VISIBLE=False),
    Bool16("shader_flags", *shader_flags),
    SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
    SEnum16("framebuffer_fade_mode", *render_fade_mode),
    Bool16("map_flags",
        "unfiltered"
        ),

    # NOTE: This field should be the only difference between
    # this particle_state desc and the hek one
    reflexive("shader_extensions",
        Struct("shader_extension", INCLUDE=os_shader_extension), 1
        ),
    Pad(16),
    #Secondary map
    Struct("secondary_map",
        dependency("bitmap", "bitm"),
        SEnum16("anchor", *render_anchor),
        Bool16("flags",
            "unfiltered"
            ),
        Struct("u_animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v_animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation_animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation_center", INCLUDE=xy_float),
        Pad(4),
        Float("zsprite_radius_scale"),
        ),

    Pad(20),
    reflexive("physics_constants", physics_constant, 16),
    SIZE=376
    )

particle_type = desc_variant(particle_type,
    ("particle_states", reflexive("particle_states",
        particle_state, 8, DYN_NAME_PATH='.name')
     )
    )

pctl_body = desc_variant(pctl_body,
    ("particle_types", reflexive("particle_types",
        particle_type, 4, DYN_NAME_PATH='.name')
     )
    )


def get():
    return pctl_def

pctl_def = TagDef("pctl",
    blam_header("pctl", 4),
    pctl_body,

    ext=".particle_system", endian=">", tag_cls=HekTag,
    )
