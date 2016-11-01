from .shdr import *
from supyr_struct.defs.tag_def import TagDef
from .objs.soso import SosoTag

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
    BFloat("perpendicular brightness"),#[0,1]
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness"),#[0,1]
    QStruct("parallel tint color",      INCLUDE=rgb_float),

    Pad(8),
    BFloat("specular Lighting exponent"),
    BFloat("specular Lighting coefficient"),
    SIZE=192,
    )


soso_body = Struct("tagdata",
    shader_attrs,

    #Model Shader Properties
    BBool16("flags",
        "detail after reflection",
        "two-sided",
        "not alpha-tested",
        "alpha-blended decal",
        "true atmospheric fog",
        "disable two-sided culling",
        ),
    Pad(14),
    BFloat("translucency"),
    
    Pad(16),
    #Color-Change
    BSEnum16("color change source", *function_names),
        
    Pad(30),
    #Self-Illumination
    Struct("self illumination",
        BBool16("flags",
            "no random phase"
            ),
        Pad(2),
        BSEnum16("color source", *function_names),
        BSEnum16("animation function", *animation_functions),
        BFloat("animation period"),#seconds
        QStruct("color lower bound", INCLUDE=rgb_float),
        QStruct("color upper bound", INCLUDE=rgb_float),
        ),
        
    Pad(12),
    #Diffuse, Multipurpose, and Detail Maps
    Struct("maps",
        BFloat("map u-scale"),
        BFloat("map v-scale"),
        dependency("diffuse map", valid_bitmaps),
           
        Pad(8),
        dependency("multipurpose map", valid_bitmaps),

        Pad(8),
        BSEnum16("detail function", *detail_map_functions),
        BSEnum16("detail mask",     *detail_mask),
           
        BFloat("detail map scale"),
        dependency("detail map", valid_bitmaps),
        BFloat("detail map v-scale"),
        ),
    
    #OS Shader Model Extension
    reflexive("os shader model ext", os_soso_ext, 1),
        
    #Texture Scrolling Animation
    Struct("texture scrolling",
        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation",   INCLUDE=anim_src_func_per_pha_sca),
        QStruct("rot-animation center", INCLUDE=xy_float),
        ),
                   
    Pad(8),
    #Reflection Properties
    Struct("reflection properties",
        BFloat("falloff distance"),#world units
        BFloat("cutoff distance"),#world units
     
        BFloat("perpendicular brightness"),#[0,1]
        QStruct("perpendicular tint color", INCLUDE=rgb_float),
        BFloat("parallel brightness"),#[0,1]
        QStruct("parallel tint color",      INCLUDE=rgb_float),

        dependency("reflection cube map map", valid_bitmaps),
        ),
    SIZE=440,
    )


def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header('soso', 2),
    soso_body,

    ext=".shader_model", endian=">"
    )
