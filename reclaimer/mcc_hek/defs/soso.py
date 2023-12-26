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

soso_comment = """MODEL SHADER
Setting <true atmospheric fog> enables per-pixel atmospheric fog but disables point/spot
lights, planar fog, and the ability to control the atmospheric fog density for this shader."""

cc_comment = """CHANGE COLOR
Change color is used to recolor the diffuse map, it affects pixels
based on the ALPHA channel (BLUE on XBOX) of the multipurpose map."""

self_illum_comment = """SELF-ILLUMINATION
Self-illumination adds diffuse light to pixels based on the GREEN channel
of the multipurpose map. The external self-illumination color referenced by
<color source> is modulated by the self-illumination animation."""

maps_comment = """MAPS
On PC, the multipurpose map channels are used for:
* RED: auxiliary mask (usually used for detail)
* GREEN: self-illumination mask (adds to diffuse light)
* BLUE: specular reflection mask (modulates reflections)
* ALPHA: color change mask (recolors diffuse map)

On XBOX, the channels are used for:
* RED: specular reflection
* GREEN: self-illumination
* BLUE: color change
* ALPHA: auxiliary

Note: When DXT1 compressed color-key textures are used for the
multipurpose map (as they should be normally), the alpha channel is 1-bit
and any non-zero alpha pixels must have zero-color, therefore on PC if we
need colorchange we use DXT3 (explicit alpha) or DXT5 (interpolated alpha).

Detail map affects diffuse map, and optionally affects reflection
if <detail after reflection> flag is set."""

tex_scroll_comment = """TEXTURE SCROLLING ANIMATIONS
Scrolls all 2D maps simultaneously."""

reflection_prop_comment = """REFLECTION PROPERTIES"""

model_shader = Struct("model_shader",
    Bool16("flags",
        "detail_after_reflection",
        "two_sided",
        "not_alpha_tested",
        "alpha_blended_decal",
        "true_atmospheric_fog",
        "disable_two_sided_culling",
        ),
    Pad(14),
    Float("translucency"),
    COMMENT=soso_comment
    )

self_illumination = Struct("self_illumination",
    Bool16("flags",
        "no_random_phase"
        ),
    Pad(2),
    SEnum16("color_source", *function_names),
    SEnum16("animation_function", *animation_functions),
    float_sec("animation_period"),  # seconds
    QStruct("color_lower_bound", INCLUDE=rgb_float),
    QStruct("color_upper_bound", INCLUDE=rgb_float),
    COMMENT=self_illum_comment
    )

maps = Struct("maps",
    Float("map_u_scale"),
    Float("map_v_scale"),
    dependency("diffuse_map", "bitm"),

    Pad(8),
    dependency("multipurpose_map", "bitm"),

    Pad(8),
    SEnum16("detail_function", *detail_map_functions),
    SEnum16("detail_mask", *detail_mask),

    Float("detail_map_scale"),
    dependency("detail_map", "bitm"),
    Float("detail_map_v_scale"),
    COMMENT=maps_comment
    )

texture_scrolling = Struct("texture_scrolling",
    Struct("u_animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v_animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation_animation", INCLUDE=anim_src_func_per_pha_sca_rot),
    QStruct("rot_animation_center", INCLUDE=xy_float),
    COMMENT=tex_scroll_comment
    )

reflection = Struct("reflection",
    float_wu("falloff_distance"),  # world units
    float_wu("cutoff_distance"),  # world units

    float_zero_to_one("perpendicular_brightness"),
    QStruct("perpendicular_tint_color", INCLUDE=rgb_float),
    float_zero_to_one("parallel_brightness"),
    QStruct("parallel_tint_color", INCLUDE=rgb_float),

    dependency("cube_map", "bitm"),
    #COMMENT=reflection_prop_comment
    )

soso_attrs = Struct("soso_attrs",
    #Model Shader Properties
    model_shader,

    Pad(16),
    #Color-Change
    SEnum16("color_change_source", *function_names, COMMENT=cc_comment),


    Pad(30),
    #Self-Illumination
    self_illumination,

    Pad(12),
    #Diffuse, Multipurpose, and Detail Maps
    maps,

    # this padding is the reflexive for the OS shader model extension
    Pad(12),

    #Texture Scrolling Animation
    texture_scrolling,

    Pad(8),
    #Reflection Properties
    reflection,
    Pad(16),

    Float("unknown0", VISIBLE=False),
    BytesRaw("unknown1", SIZE=16, VISIBLE=False),  # little endian dependency

    SIZE=400
    )


soso_body = Struct("tagdata",
    shdr_attrs,
    soso_attrs
    )


def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header('soso', 2),
    soso_body,

    ext=".shader_model", endian=">", tag_cls=ShdrTag
    )
