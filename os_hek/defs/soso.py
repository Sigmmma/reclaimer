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

os_soso_ext = Struct("shader model extension",
    #Specular Color
    dependency_os("specular color map", "bitm", COMMENT=specular_map_comment),
    Float("specular color coefficient"),
    Pad(4),
    Float("specular color exponent"),
    Bool16("flags",
        "alpha as exponent mask",
        ),

    Pad(2),
    #Base Normal Map
    dependency_os("base normal map", "bitm", COMMENT=normal_maps_comment),
    Float("base normal coefficient"),

    Pad(12),
    #Detail Normal Maps
    dependency_os("detail normal 1 map", "bitm"),
    Float("detail normal 1 coefficient"),
    Float("detail normal 1 scale"),
    Float("detail normal 1 v-scale"),

    Pad(4),
    dependency_os("detail normal 2 map", "bitm"),
    Float("detail normal 2 coefficient"),
    Float("detail normal 2 scale"),
    Float("detail normal 2 v-scale"),

    Pad(4),
    #Specular Tint Override
    float_zero_to_one("perpendicular brightness", COMMENT=specular_tint_override_comment),
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    float_zero_to_one("parallel brightness"),
    QStruct("parallel tint color", INCLUDE=rgb_float),

    Bool16("diffuse lighting flags",
        { NAME: "do_not_use_dlms", GUI_NAME: "do not use dlms (bsp)" },
        COMMENT=diffuse_lighting_comment
        ),
    Pad(4),
    Pad(2),

    Float("specular Lighting exponent", COMMENT=specular_lighting_comment),
    Float("specular Lighting coefficient"),
    SIZE=192,
    )

soso_attrs = Struct("soso attrs",
    #Model Shader Properties
    model_shader,

    Pad(16),
    #Color-Change
    SEnum16("color change source", *function_names, COMMENT=cc_comment),

    Pad(30),
    #Self-Illumination
    self_illumination,

    Pad(12),
    #Diffuse, Multipurpose, and Detail Maps
    maps,

    reflexive("os shader model ext", os_soso_ext, 1),

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

    ext=".shader_model", endian=">", tag_cls=HekTag
    )
