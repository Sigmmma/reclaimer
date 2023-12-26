#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .schi import *
from supyr_struct.defs.tag_def import TagDef
from .objs.shdr import ShdrTag

chicago_2_stage_maps = Struct("two_stage_map", INCLUDE=chicago_4_stage_maps)

scex_attrs = Struct("scex_attrs",
    # Shader Properties
    Struct("chicago_shader_extended",
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
    reflexive("four_stage_maps", chicago_4_stage_maps, 4,
        DYN_NAME_PATH='.bitmap.filepath'),
    reflexive("two_stage_maps", chicago_2_stage_maps, 2,
        DYN_NAME_PATH='.bitmap.filepath'),
    Bool32("extra_flags",
        "dont_fade_active_camouflage",
        "numeric_countdown_timer"
        ),
    SIZE=80
    )

scex_body = Struct("tagdata",
    shdr_attrs,
    scex_attrs,
    SIZE=120
    )


def get():
    return scex_def

scex_def = TagDef("scex",
    blam_header('scex'),
    scex_body,

    ext=".shader_transparent_chicago_extended",
    endian=">", tag_cls=ShdrTag
    )
