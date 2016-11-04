from ...hek.defs.soso import *

os_soso_ext = Struct("shader model extension",
    #Specular Color
    dependency("specular color map", valid_bitmaps),
    BFloat("specular color coefficient"),
    Pad(4),
    BFloat("specular color exponent"),
    BBool16("flags",
        "alpha as exponent mask",
        ),
                     
    Pad(2),
    #Base Normal Map
    dependency("base normal map", valid_bitmaps),
    BFloat("base normal coefficient"),

    Pad(12),
    #Detail Normal Maps
    dependency("detail normal 1 map", valid_bitmaps),
    BFloat("detail normal 1 coefficient"),
    BFloat("detail normal 1 scale"),
    BFloat("detail normal 1 v-scale"),

    Pad(4),
    dependency("detail normal 2 map", valid_bitmaps),
    BFloat("detail normal 2 coefficient"),
    BFloat("detail normal 2 scale"),
    BFloat("detail normal 2 v-scale"),

    Pad(4),
    #Specular Tint Override
    BFloat("perpendicular brightness", MIN=0.0, MAX=1.0),
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness", MIN=0.0, MAX=1.0),
    QStruct("parallel tint color", INCLUDE=rgb_float),

    Pad(8),
    BFloat("specular Lighting exponent"),
    BFloat("specular Lighting coefficient"),
    SIZE=192,
    )

# replace the padding with an open sauce shader model extension reflexive
soso_attrs = dict(soso_attrs)
soso_attrs[9] = reflexive("os shader model ext", os_soso_ext, 1)

soso_body = Struct("tagdata",
    shdr_attrs,
    soso_attrs,
    SIZE=440
    )

def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header('soso', 2),
    soso_body,

    ext=".shader_model", endian=">"
    )
