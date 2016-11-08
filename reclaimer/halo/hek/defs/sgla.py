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
    QStruct("background tint color", INCLUDE=rgb_float),
    BFloat("background tint map scale"),
    dependency("background tint map", "bitm"),

    Pad(22),
    #Reflection Properties
    BSEnum16("reflection type",
        "bumped cubemap",
        "flat cubemap",
        "dynamic mirror",
        ),
    BFloat("perpendicular brightness"),#[0,1]
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness"),#[0,1]
    QStruct("parallel tint color", INCLUDE=rgb_float),
    dependency("reflection map", "bitm"),

    BFloat("bump map scale"),
    dependency("bump map", "bitm"),

    Pad(132),
    #Diffuse Properties
    BFloat("diffuse map scale"),
    dependency("diffuse map", "bitm"),
    BFloat("diffuse detail map scale"),
    dependency("diffuse detail map", "bitm"),

    Pad(32),
    #Specular Properties
    BFloat("specular map scale"),
    dependency("specular map", "bitm"),
    BFloat("specular detail map scale"),
    dependency("specular detail map", "bitm"),
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
