from ...hek.defs.soso import *

os_soso_ext = Struct("shader model extension",
    #Specular Color
    dependency_os("specular color map", "bitm"),
    Float("specular color coefficient"),
    Pad(4),
    Float("specular color exponent"),
    Bool16("flags",
        "alpha as exponent mask",
        ),
                     
    Pad(2),
    #Base Normal Map
    dependency_os("base normal map", "bitm"),
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
    float_zero_to_one("perpendicular brightness"),
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    float_zero_to_one("parallel brightness"),
    QStruct("parallel tint color", INCLUDE=rgb_float),

    SInt16("unknown0", VISIBLE=False),
    SInt16("unknown1", VISIBLE=False),
    FlFloat("unknown2", VISIBLE=False),
    Float("specular Lighting exponent"),
    Float("specular Lighting coefficient"),
    SIZE=192,
    )

soso_attrs = Struct("soso attrs",
    #Model Shader Properties
    model_shader,

    Pad(16),
    #Color-Change
    SEnum16("color change source", *function_names),

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
    reflection_properties,
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
