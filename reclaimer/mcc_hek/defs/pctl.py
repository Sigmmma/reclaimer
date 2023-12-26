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

particle_creation_physics = (
    "default",
    "explosion",
    "jet"
    )

physics_constant = QStruct("physics_constant",
    Float("k", UNIT_SCALE=per_sec_unit_scale),
    )

state = Struct("state",
    ascii_str32("name"),
    from_to_sec("duration_bounds"),
    from_to_sec("transition_time_bounds"),

    Pad(4),
    Float("scale_multiplier"),
    Float("animation_rate_multiplier"),
    Float("rotation_rate_multiplier"),
    QStruct("color_multiplier", INCLUDE=argb_float),
    Float("radius_multiplier"),
    Float("minimum_particle_count"),
    Float("particle_creation_rate",
           SIDETIP="particles/sec", UNIT_SCALE=per_sec_unit_scale),

    Pad(84),
    SEnum16("particle_creation_physics", *particle_creation_physics),
    Pad(2),  # SEnum16("particle_update_physics", "default"),
    reflexive("physics_constants", physics_constant, 16),
    SIZE=192
    )

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

    Pad(12),  # open sauce particle shader extension
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


particle_type = Struct("particle_type",
    ascii_str32("name"),
    Bool32("flags",
        "type_states_loop",
        "type_states_loops_forward_backward",
        "particle_states_loop",
        "particle_states_loops_forward_backward",
        "particles_die_in_water",
        "particles_die_in_air",
        "particles_die_on_ground",
        "rotational_sprites_animate_sideways",
        "disabled",
        "tint_by_effect_color",
        "initial_count_scales_with_effect",
        "minimum_count_scales_with_effect",
        "creation_rate_scales_with_effect",
        "radius_scales_with_effect",
        "animation_rate_scales_with_effect",
        "rotation_rate_scales_with_effect",
        "dont_draw_in_first_person",
        "dont_draw_in_third_person",
        ),
    SInt16("initial_particle_count"),

    Pad(2),
    SEnum16("complex_sprite_render_modes",
        "simple",
        "rotational"
        ),

    Pad(2),
    float_wu("radius"),

    Pad(36),
    SEnum16("particle_creation_physics", *particle_creation_physics),

    Pad(6),
    reflexive("physics_constants", physics_constant, 16),
    reflexive("states", state, 8, DYN_NAME_PATH='.name'),
    reflexive("particle_states", particle_state, 8, DYN_NAME_PATH='.name'),
    SIZE=128
    )

pctl_body = Struct("tagdata",
    Pad(56),
    dependency("point_physics", "pphy"),
    SEnum16("system_update_physics",
        "default",
        "explosion"
        ),
    Pad(6),
    reflexive("physics_constants", physics_constant, 16),
    reflexive("particle_types", particle_type, 4, DYN_NAME_PATH='.name'),
    SIZE=104,
    )


def get():
    return pctl_def

pctl_def = TagDef("pctl",
    blam_header("pctl", 4),
    pctl_body,

    ext=".particle_system", endian=">", tag_cls=HekTag,
    )
