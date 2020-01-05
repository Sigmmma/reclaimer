#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .shdr import *
from supyr_struct.defs.tag_def import TagDef
from .objs.shdr import ShdrTag

chicago_4_stage_maps = Struct("four_stage_map",
    Bool16("flags" ,
        "unfiltered",
        "alpha_replicate",
        "u_clamped",
        "v_clamped",
        ),

    Pad(42),
    SEnum16("color_function", *blend_functions),
    SEnum16("alpha_function", *blend_functions),

    Pad(36),
    #shader transformations
    Float("map_u_scale"),
    Float("map_v_scale"),
    Float("map_u_offset"),
    Float("map_v_offset"),
    float_deg("map_rotation"),  # degrees
    float_zero_to_one("map_bias"),  # [0,1]
    dependency("bitmap", "bitm"),

    #shader animations
    Pad(40),
    Struct("u_animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v_animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation_animation", INCLUDE=anim_src_func_per_pha_sca_rot),

    QStruct("rotation_center", INCLUDE=xy_float),
    SIZE=220,
    )

schi_attrs = Struct("schi_attrs",
    # Shader Properties
    Struct("chicago_shader",
        UInt8("numeric_counter_limit",
            MIN=0, MAX=255, SIDETIP="[0,255]"),  # [0,255]

        Bool8("chicago_shader_flags", *trans_shdr_properties),
        SEnum16("first_map_type", *trans_shdr_first_map_type),
        SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
        SEnum16("framebuffer_fade_mode", *render_fade_mode),
        SEnum16("framebuffer_fade_source", *function_outputs),
        Pad(2),
        ),

    #Lens Flare
    float_wu("lens_flare_spacing"),  # world units
    dependency("lens_flare", "lens"),
    reflexive("extra_layers", extra_layers_block, 4,
        DYN_NAME_PATH='.filepath'),
    reflexive("maps", chicago_4_stage_maps, 4,
        DYN_NAME_PATH='.bitmap.filepath'),
    Bool32("extra_flags",
        "dont_fade_active_camouflage",
        "numeric_countdown_timer"
        ),
    SIZE=68
    )

schi_body = Struct("tagdata",
    shdr_attrs,
    schi_attrs,
    SIZE=108
    )


def get():
    return schi_def

schi_def = TagDef("schi",
    blam_header('schi'),
    schi_body,

    ext=".shader_transparent_chicago",
    endian=">", tag_cls=ShdrTag
    )
