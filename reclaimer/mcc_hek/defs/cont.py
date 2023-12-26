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

def get(): return cont_def

point_state = Struct("point_state",
    from_to_sec("state_duration"),
    from_to_sec("state_transition_duration"),
    dependency("physics", "pphy"),
    Pad(32),
    float_wu("width"),
    QStruct("color_lower_bound", INCLUDE=argb_float),
    QStruct("color_upper_bound", INCLUDE=argb_float),
    Bool32("scale_flags",
        "duration",
        "duration_delta",
        "transition_duration",
        "transition_duration_delta",
        "color",
        ),
    SIZE=104
    )

cont_body = Struct("tagdata",
    Bool16("flags",
        "first_point_unfaded",
        "last_point_unfaded",
        "points_start_pinned_to_media",
        "points_start_pinned_to_ground",
        "points_always_pinned_to_media",
        "points_always_pinned_to_ground",
        "edge_effect_fades_slowly",
        ),
    Bool16("scale_flags",
        "point_generation_rate",
        "point_velocity",
        "point_velocity_delta",
        "point_velocity_cone_angle",
        "inherited_velocity_fraction",
        "sequence_animation_rate",
        "texture_scale_u",
        "texture_scale_v",
        "texture_animation_u",
        "texture_animation_v",
        ),

    Struct("point_creation",
        Float("generation_rate",
               SIDETIP="points/sec", UNIT_SCALE=per_sec_unit_scale),
        from_to_wu_sec("velocity"),
        float_rad("velocity_cone_angle"),
        Float("inherited_velocity_fraction"),
        ),

    Struct("rendering",
        SEnum16("render_type",
            "vertical_orientation",
            "horizontal_orientation",
            "media_mapped",
            "ground_mapped",
            "viewer_facing",
            "double_marker_linked",
            ),
        Pad(2),
        Float("texture_repeats_u"),
        Float("texture_repeats_v"),

        Float("texture_animation_u", SIDETIP="repeats/sec"),
        Float("texture_animation_v", SIDETIP="repeats/sec"),
        Float("animation_rate", SIDETIP="frames/sec"),
        dependency("bitmap", "bitm"),
        SInt16("first_sequence_index"),
        SInt16("sequence_count"),
        Pad(100),

        FlUInt32("unknown0", VISIBLE=False),
        Bool16("shader_flags", *shader_flags),
        SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
        SEnum16("framebuffer_fade_mode", *render_fade_mode),
        Bool16("map_flags",
            "unfiltered",
            ),
        ),
    Pad(12),  # OS v4 shader extension padding
    Pad(16),

    Struct("secondary_map",
        dependency("bitmap", "bitm"),
        SEnum16("anchor", *render_anchor),
        Bool16("map_flags",
            "unfiltered",
            ),

        Struct("u_animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v_animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation_animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation_center", INCLUDE=xy_float),
        Pad(4),
        Float("zsprite_radius_scale"),
        Pad(20),
        ),
    reflexive("point_states", point_state, 16),
    SIZE=324,
    )

cont_def = TagDef("cont",
    blam_header('cont', 3),
    cont_body,

    ext=".contrail", endian=">", tag_cls=HekTag
    )
