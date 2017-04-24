from .shdr import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef


model_shader = Struct("model shader",
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
    )
        
self_illumination = Struct("self illumination",
    BBool16("flags",
        "no random phase"
        ),
    Pad(2),
    BSEnum16("color source", *function_names),
    BSEnum16("animation function", *animation_functions),
    float_sec("animation period"),  # seconds
    QStruct("color lower bound", INCLUDE=rgb_float),
    QStruct("color upper bound", INCLUDE=rgb_float),
    )
        
maps = Struct("maps",
    BFloat("map u-scale"),
    BFloat("map v-scale"),
    dependency("diffuse map", "bitm"),
       
    Pad(8),
    dependency("multipurpose map", "bitm"),

    Pad(8),
    BSEnum16("detail function", *detail_map_functions),
    BSEnum16("detail mask", *detail_mask),
       
    BFloat("detail map scale"),
    dependency("detail map", "bitm"),
    BFloat("detail map v-scale"),
    )

texture_scrolling = Struct("texture scrolling",
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
    QStruct("rot-animation center", INCLUDE=xy_float),
    )
                   

reflection_properties = Struct("reflection properties",
    float_wu("falloff distance"),  # world units
    float_wu("cutoff distance"),  # world units
 
    float_zero_to_one("perpendicular brightness"),
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    float_zero_to_one("parallel brightness"),
    QStruct("parallel tint color", INCLUDE=rgb_float),

    dependency("reflection cube map map", "bitm"),
    )

soso_attrs = Struct("soso attrs",
    #Model Shader Properties
    model_shader,
        
    Pad(16),
    #Color-Change
    BSEnum16("color change source", *function_names),
        
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
    reflection_properties,
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
