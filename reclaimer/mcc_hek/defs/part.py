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

part_body = Struct("tagdata",
    Bool32("flags",
        "can_animate_backwards",
        "animation_stops_at_rest",
        "animation_starts_on_random_frame",
        "animate_once_per_frame",
        "dies_at_rest",
        "dies_on_contact_with_structure",
        "tint_from_diffuse_texture",
        "dies_on_contact_with_water",
        "dies_on_contact_with_air",
        "self_illuminated",
        "random_horizontal_mirroring",
        "random_vertical_mirroring",
        ),
    dependency("bitmap", "bitm"),
    dependency("physics", "pphy"),
    dependency("impact_effect", "foot",
        TOOLTIP="Marty traded his kids for this"),

    Pad(4),
    from_to_sec("lifespan"),
    float_sec("fade_in_time"),
    float_sec("fade_out_time"),

    dependency("collision_effect", valid_event_effects),
    dependency("death_effect", valid_event_effects),

    Struct("rendering",
        Float("minimum_size", SIDETIP="pixels"),
        FlSInt32("unknown0", VISIBLE=False),
        FlFloat("unknown1", VISIBLE=False),
        QStruct("radius_animation", INCLUDE=from_to),
        Pad(4),
        QStruct("animation_rate",
            Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
            Float("to",   UNIT_SCALE=per_sec_unit_scale),
            ORIENT='h', SIDETIP='frames/sec'
            ),
        Float("contact_deterioration"),
        Float("fade_start_size", SIDETIP="pixels"),
        Float("fade_end_size", SIDETIP="pixels"),

        Pad(4),
        SInt16("first_sequence_index"),
        SInt16("initial_sequence_count"),
        SInt16("looping_sequence_count"),
        SInt16("final_sequence_count"),

        Pad(12),
        SEnum16("orientation", *render_mode),

        Pad(38),
        FlUInt32("unknown2", VISIBLE=False),
        Bool16("shader_flags", *shader_flags),
        SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
        SEnum16("framebuffer_fade_mode", *render_fade_mode),
        Bool16("map_flags",
            "unfiltered"
            ),
        ),
    Pad(12),  # OS v4 shader extension padding
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

    SIZE=356,
    )


def get():
    return part_def

part_def = TagDef("part",
    blam_header("part", 2),
    part_body,

    ext=".particle", endian=">", tag_cls=HekTag,
    )
