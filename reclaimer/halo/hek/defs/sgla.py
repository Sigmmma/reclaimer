from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

sgla_body = Struct("tagdata",
    #Radiosity Properties
    radiosity_settings,

    #Shader Type
    material_type,
    shader_id_num,

    Pad(2),
    #Environment Shader Properties
    BBool16("glass shader flags",
        "alpha tested",
        "decal",
        "two-sided",
        "bump map is specular mask",
        ),

    Pad(42),
    #Background Tint Properties
    Struct("background tint color", INCLUDE=rgb_float),
    BFloat("background tint map scale"),
    dependency("background tint map", valid_bitmaps),

    Pad(22),
    #Reflection Properties
    BSEnum16("reflection type",
        "bumped Cubemap",
        "flat Cubemap",
        "dynamic Mirror",
        ),
    BFloat("perpendicular brightness"),#[0,1]
    Struct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color", INCLUDE=rgb_float),
    dependency("reflection map", valid_bitmaps),

    BFloat("bump map scale"),
    dependency("bump map", valid_bitmaps),

    Pad(132),
    #Diffuse Properties
    BFloat("diffuse map scale"),
    dependency("diffuse map", valid_bitmaps),
    BFloat("diffuse detail map scale"),
    dependency("diffuse detail map", valid_bitmaps),

    Pad(32),
    #Specular Properties
    BFloat("specular map scale"),
    dependency("specular map", valid_bitmaps),
    BFloat("specular detail map scale"),
    dependency("specular detail map", valid_bitmaps),

    SIZE=480,
    )


def get():
    return sgla_def

sgla_def = TagDef("sgla",
    blam_header('sgla'),
    sgla_body,

    ext=".shader_glass", endian=">"
    )
