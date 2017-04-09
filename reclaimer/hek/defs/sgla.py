from .shdr import *
from supyr_struct.defs.tag_def import TagDef

sgla_attrs = Struct("sgla attrs",
    #Environment Shader Properties
    BBool16("glass shader flags",
        "alpha tested",
        "decal",
        "two-sided",
        "bump map is specular mask",
        ),

    Pad(42),
    #Background Tint Properties
    Struct("background tint properties",
        QStruct("color", INCLUDE=rgb_float),
        BFloat("map scale"),
        dependency("map", "bitm"),
        ),

    Pad(22),
    #Reflection Properties
    Struct("reflection properties",
        BSEnum16("type",
            "bumped cubemap",
            "flat cubemap",
            "dynamic mirror",
            ),
        float_zero_to_one("perpendicular brightness"),  # [0,1]
        QStruct("perpendicular tint color", INCLUDE=rgb_float),
        float_zero_to_one("parallel brightness"),  # [0,1]
        QStruct("parallel tint color", INCLUDE=rgb_float),
        dependency("map", "bitm"),

        BFloat("bump map scale"),
        dependency("bump map", "bitm"),
        ),

    Pad(132),
    #Diffuse Properties
    Struct("diffuse properties",
        BFloat("map scale"),
        dependency("map", "bitm"),
        BFloat("detail map scale"),
        dependency("detail map", "bitm"),
        ),

    Pad(32),
    #Specular Properties
    Struct("specular properties",
        BFloat("map scale"),
        dependency("map", "bitm"),
        BFloat("detail map scale"),
        dependency("detail map", "bitm"),
        ),
    SIZE=440
    )

sgla_body = Struct("tagdata",
    shdr_attrs,
    sgla_attrs,
    SIZE=480,
    )


def get():
    return sgla_def

sgla_def = TagDef("sgla",
    blam_header('sgla'),
    sgla_body,

    ext=".shader_transparent_glass", endian=">"
    )