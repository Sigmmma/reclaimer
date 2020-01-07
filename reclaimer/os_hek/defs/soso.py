#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.soso import *

specular_map_comment = """SPECULAR (COLOR) MAP
The specular color map is multiplied by the stock specular
to provide finer control over specular color.

*RGB holds the specular color.
*ALPHA can be used as an exponent mask to provide finer control
over the size of the specular highlights."""

normal_maps_comment = """NORMAL MAPS
*RED holds the horizontal normal data.
*GREEN holds the vertical normal data.
*BLUE holds the 'height', dimmer blue means dimmer specular and reflection.

*ALPHA is used for detail normal opacity:
A = no detail normal maps visible
B = detail normal 1 at full opacity
C = detail normal 2 at full opacity
D = also no detail normal maps visible

alpha brightness:
   A -------> B -------> C -------> D
  0/0.000   85/0.333  170/0.666  255/1.000

Normal coefficient is used to change the height/visiblity of the normal map."""

specular_tint_override_comment = """SPECULAR TINT OVERRIDE
These values override the specular tint colors in the stock part of the tag (the bottom).
Useful for if you want to have specific os and non-os tint values.

(Whetever these values are used is controlled by if the user has opensauce,
not by the opensauce settings.)"""

diffuse_lighting_comment = """DIFFUSE LIGHTING"""

specular_lighting_comment = """SPECULAR LIGHTING
Exponent controls the highlight size, the bigger the exponent, the smaller the highlight.
Coefficient controls the brightness of the highlights."""

os_reflection_prop_comment = """REFLECTION PROPERIES
When the opensauce extension is used the tint values in here are overwritten
by the ones in the os extension when the map is loaded."""

reflection = Struct("reflection",
    INCLUDE=reflection, COMMENT=os_reflection_prop_comment
    )

os_soso_ext = Struct("shader_model_extension",
    #Specular Color
    dependency_os("specular_color_map", "bitm", COMMENT=specular_map_comment),
    Float("specular_color_coefficient"),
    Pad(4),
    Float("specular_color_exponent"),
    Bool16("flags",
        "alpha_as_exponent_mask",
        ),

    Pad(2),
    #Base Normal Map
    dependency_os("base_normal_map", "bitm", COMMENT=normal_maps_comment),
    Float("base_normal_coefficient"),

    Pad(12),
    #Detail Normal Maps
    dependency_os("detail_normal_1_map", "bitm"),
    Float("detail_normal_1_coefficient"),
    Float("detail_normal_1_scale"),
    Float("detail_normal_1_v_scale"),

    Pad(4),
    dependency_os("detail_normal_2_map", "bitm"),
    Float("detail_normal_2_coefficient"),
    Float("detail_normal_2_scale"),
    Float("detail_normal_2_v_scale"),

    Pad(4),
    #Specular Tint Override
    float_zero_to_one("perpendicular_brightness", COMMENT=specular_tint_override_comment),
    QStruct("perpendicular_tint_color", INCLUDE=rgb_float),
    float_zero_to_one("parallel_brightness"),
    QStruct("parallel_tint_color", INCLUDE=rgb_float),

    Bool16("diffuse_lighting_flags",
        { NAME: "do_not_use_dlms", GUI_NAME: "do not use dlms (bsp)" },
        COMMENT=diffuse_lighting_comment
        ),
    Pad(4),
    Pad(2),

    Float("specular_lighting_exponent", COMMENT=specular_lighting_comment),
    Float("specular_lighting_coefficient"),
    SIZE=192,
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

    reflexive("os_shader_model_ext", os_soso_ext, 1),

    #Texture Scrolling Animation
    texture_scrolling,

    Pad(8),
    #Reflection Properties
    reflection,
    Pad(16),

    FlFloat("unknown0", VISIBLE=False),
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
