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

environment_shader_comment = """ENVIRONMENT SHADER
Setting <true atmospheric fog> enables per-pixel atmospheric fog (for models) but disables
point/spot lights, planar fog, and the ability to control the atmospheric fog density for
this shader.

Alpha-tested controls if the shader is masked by the diffuse alpha (or depending on
the environment shader type's setting) the bump map alpha. The transparancy is only 1-bit"""

environment_shader_type_comment = """ENVIRONMENT SHADER TYPE
Controls how diffuse maps are combined:

NORMAL:
Secondary detail map alpha controls blend between primary and secondary detail map.
Specular mask is alpha of blended primary and secondary detail map alpha multiplied by
alpha of micro detail map.

BLENDED:
Base map alpha controls blend between primary and secondary detail map.
Specular mask is alpha of blended primary and secondary detail map alpha multiplied by
alpha of micro detail map.

BLENDED BASE SPECULAR:
Same as BLENDED, except specular mask is alpha is base map multiplied with
the alpha of micro detail map."""

bump_properties_comment = """BUMP PROPERTIES
Perforated (alpha-tested) shaders use alpha in bump map."""

tex_scroll_anim_comment = """TEXTURE SCROLLING ANIMATION
Scrolls all 2D maps simultaneously."""

self_illum_comment = """SELF-ILLUMINATION PROPERTIES
There are three self-illumination effects which are added together.
Each effect has an <on color>, used when the shader is active, and an <off color>, used when
the shader is not active. The self-illumination map is used as follows:
* RED: primary mask
* GREEN: secondary mask
* BLUE: plasma mask
* ALPHA: plasma animation reference

Each effect also has an animation <function>, <period> and <phase>, used when the shader is
active. The primary and secondary effects simply modulate the <on color> by the animation
value to produce an animation color, and then blend between the animation color and the
<off color> based on the shader's activation level, and finally modulate by the mask.

The plasma shader compares the animation value with the alpha channel of the map (the plasma
animation reference) and produces a high value when they are similar and a dark value when
they are different. This value modulates the <plasma on color> to produce a plasma animation
color, and the rest proceeds just like the primary and secondary effects."""

specular_properties_comment = """SPECULAR PROPERTIES
Controls the dynamic specular highlights. The highlight is modulated by brightness
and a blend between perpendicular and parrallel color.

These color values also affect the colour of the reflection in REFLECTION PROPERTIES"""

reflection_properties_comment = """REFLECTION PROPERTIES
Controls cube map reflections. The color of the cubemap is tinted by the color settings
in the SPECULAR PROPERTIES and the brightness in the REFLECTION PROPERTIES.

BUMPED CUBE MAP: Makes it so that the reflection and fresnel is affected by the bump map.

FLAT CUBE MAP: The reflection is not affected by the cubemap, the fresnel still is though."""

environment_shader = Struct("environment_shader",
    Bool16("flags",
        "alpha_tested",
        "bump_map_is_specular_mask",
        "true_atmospheric_fog",
        COMMENT=environment_shader_comment
        ),
    SEnum16("type",
        "normal",
        "blended",
        "blended_base_specular",
        COMMENT=environment_shader_type_comment
        ),
    )

diffuse = Struct("diffuse",
    Bool16("diffuse_flags",
        "rescale_detail_maps",
        "rescale_bump_maps",
        ),
    Pad(26),
    dependency("base_map", "bitm"),

    Pad(24),
    SEnum16("detail_map_function", *detail_map_functions),
    Pad(2),

    Float("primary_detail_map_scale"),
    dependency("primary_detail_map", "bitm"),
    Float("secondary_detail_map_scale"),
    dependency("secondary_detail_map", "bitm"),

    Pad(24),
    SEnum16("micro_detail_map_function", *detail_map_functions),

    Pad(2),
    Float("micro_detail_map_scale"),
    dependency("micro_detail_map", "bitm"),
    QStruct("material_color", INCLUDE=rgb_float),
    )

bump_properties = Struct("bump_properties",
    Float("map_scale"),
    dependency("map", "bitm"),
    FlFloat("map_scale_x", VISIBLE=False),
    FlFloat("map_scale_y", VISIBLE=False),
    COMMENT=bump_properties_comment
    )

texture_scrolling = Struct("texture_scrolling",
    anim_func_per_sca_macro("u_animation"),
    anim_func_per_sca_macro("v_animation"),
    COMMENT=tex_scroll_anim_comment
    )

self_illumination = Struct("self_illumination",
    Bool16("flags",
        "unfiltered",
        ),
    Pad(2),
    Pad(24),

    QStruct("primary_on_color",  INCLUDE=rgb_float),
    QStruct("primary_off_color", INCLUDE=rgb_float),
    anim_func_per_pha_macro("primary_animation"),

    Pad(24),
    QStruct("secondary_on_color",  INCLUDE=rgb_float),
    QStruct("secondary_off_color", INCLUDE=rgb_float),
    anim_func_per_pha_macro("secondary_animation"),

    Pad(24),
    QStruct("plasma_on_color",  INCLUDE=rgb_float),
    QStruct("plasma_off_color", INCLUDE=rgb_float),
    anim_func_per_pha_macro("plasma_animation"),

    Pad(24),
    Float("map_scale"),
    dependency("map", "bitm"),
    COMMENT=self_illum_comment
    )

specular = Struct("specular",
    Bool16("specular_flags",
        "overbright",
        "extra_shiny",
        "lightmap_is_specular"
        ),
    Pad(18),
    float_zero_to_one("brightness"),  # [0,1]

    Pad(20),
    QStruct("perpendicular_tint_color", INCLUDE=rgb_float),
    QStruct("parallel_tint_color",      INCLUDE=rgb_float),
    COMMENT=specular_properties_comment
    )

reflection = Struct("reflection",
    Bool16("reflection_flags",
        "dynamic_mirror",
         ),
    SEnum16("reflection_type",
        "bumped_cubemap",
        "flat_cubemap",
        "bumped_radiosity",
        ),

    float_zero_to_one("lightmap_brightness_scale"),  # [0,1]
    Pad(28),
    float_zero_to_one("perpendicular_brightness"),  # [0,1]
    float_zero_to_one("parallel_brightness"),  # [0,1]

    Pad(40),
    dependency("cube_map", "bitm"),
    COMMENT=reflection_properties_comment
    )

senv_attrs = Struct("senv_attrs",
    #Environment Shader Properties
    environment_shader,

    #Lens Flare
    float_wu("lens_flare_spacing"),  # world units
    dependency("lens_flare", "lens"),

    # this padding is the reflexive for the OS shader environment extension
    Pad(12),

    Pad(32),
    #Diffuse Properties
    diffuse,

    Pad(12),
    #Bump Properties
    bump_properties,

    Pad(16),
    #Texture Animation
    texture_scrolling,

    Pad(24),
    #Self Illumination
    self_illumination,

    Pad(24),
    #Specular Properties
    specular,

    Pad(16),
    #Reflection Properties
    reflection,
    SIZE=796
    )

senv_body = Struct("tagdata",
    shdr_attrs,
    senv_attrs,
    SIZE=836,
    )


def get():
    return senv_def

senv_def = TagDef("senv",
    blam_header('senv', 2),
    senv_body,

    ext=".shader_environment", endian=">", tag_cls=ShdrTag
    )
