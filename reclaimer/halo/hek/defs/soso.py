from .shdr import *
from supyr_struct.defs.tag_def import TagDef

soso_attrs = Struct("soso attrs",
    #Model Shader Properties
    Struct("model shader",
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
        ),
        
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
        float_sec("animation period"),  # seconds
        QStruct("color lower bound", INCLUDE=rgb_float),
        QStruct("color upper bound", INCLUDE=rgb_float),
        ),
        
    Pad(12),
    #Diffuse, Multipurpose, and Detail Maps
    Struct("maps",
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
        ),

    # this padding is the reflexive for the OS shader model extension
    Pad(12),

    #Texture Scrolling Animation
    Struct("texture scrolling",
        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rot-animation center", INCLUDE=xy_float),
        ),
                   
    Pad(8),
    #Reflection Properties
    Struct("reflection properties",
        float_wu("falloff distance"),  # world units
        float_wu("cutoff distance"),  # world units
     
        float_zero_to_one("perpendicular brightness"),
        QStruct("perpendicular tint color", INCLUDE=rgb_float),
        float_zero_to_one("parallel brightness"),
        QStruct("parallel tint color", INCLUDE=rgb_float),

        dependency("reflection cube map map", "bitm"),
        ),
    SIZE=400
    )

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
