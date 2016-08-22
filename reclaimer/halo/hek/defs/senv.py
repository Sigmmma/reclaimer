from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from .objs.senv import SenvTag

senv_body = Struct("tagdata",
    #Radiosity Properties
    radiosity_settings,

    #Shader Type
    material_type,
    FlSEnum16("numeric shader id", DEFAULT=3,
              INCLUDE=shader_id_num),
    Pad(2),
    
    #Environment Shader Properties
    BBool16("environment shader flags",
        "alpha tested",
        "bump-map is specular mask",
        "true atmospheric fog",
        ),
    BSEnum16("environment shader type",
        "normal",
        "blended",
        "blended base specular",
        ),

    #Lens Flare
    BFloat("lens flare spacing"),#world units
    dependency("lens flare"),
    Pad(44),

    #Diffuse Properties
    BBool16("diffuse flags",
        "rescale detail maps",
        "rescale bump maps",
        ),
    Pad(26),
    dependency("base map", valid_bitmaps),
                   
    Pad(24),
    BSEnum16(  "detail map function", *detail_map_functions),
    Pad(2),
    BFloat(    "primary detail map scale"),
    dependency("primary detail map", valid_bitmaps),
    BFloat(    "secondary detail map scale"),
    dependency("secondary detail map", valid_bitmaps),
    Pad(24),
    BSEnum16(  "micro detail map function", *detail_map_functions),
    Pad(2),
    BFloat(    "micro detail map scale"),
    dependency("micro detail map", valid_bitmaps),
                   
    QuickStruct("material color", INCLUDE=rgb_float),

    Pad(12),
    #Bump Properties
    BFloat("bump map scale"),
    dependency("bump map", valid_bitmaps),
    FlFloat("bump map scale x"),
    FlFloat("bump map scale y"),

    Pad(16),
    #Texture Animation
    Struct("u-animation", INCLUDE=anim_func_per_sca),
    Struct("V-animation", INCLUDE=anim_func_per_sca),

    Pad(52),
    #Self Illumination
    QuickStruct("primary on-color",  INCLUDE=rgb_float),
    QuickStruct("primary off-color", INCLUDE=rgb_float),
    Struct("primary animation", INCLUDE=anim_func_per_pha),

    Pad(24),
    QuickStruct("secondary on-color",  INCLUDE=rgb_float),
    QuickStruct("secondary off-color", INCLUDE=rgb_float),
    Struct("secondary animation", INCLUDE=anim_func_per_pha),

    Pad(24),
    QuickStruct("plasma on-color",  INCLUDE=rgb_float),
    QuickStruct("plasma off-color", INCLUDE=rgb_float),
    Struct("plasma animation", INCLUDE=anim_func_per_pha),

    Pad(24),
    BFloat("illumination map scale"),
    dependency("illumination map", valid_bitmaps),

    Pad(24),
    #Specular Properties
    BBool16("specular flags",
        "overbright",
        "extra-shiny",
        "lightmap is specular"
        ),
    Pad(18),
    BFloat("brightness"),#[0,1]

    Pad(20),
    QuickStruct("perpendicular color", INCLUDE=rgb_float),
    QuickStruct("parallel color",      INCLUDE=rgb_float),

    Pad(16),
    #Reflection Properties
    BBool16("reflection flags",
        "dynamic mirror",
         ),
    BSEnum16("reflection type",
        "bumped cubemap",
        "flat cubemap",
        "bumped radiosity",
        ),

    BFloat("lightmap brightness scale"),#[0,1]
    Pad(28),
    BFloat("perpendicular brightness"),#[0,1]
    BFloat("parallel brightness"),#[0,1]

    Pad(40),
    dependency("reflection cube map", valid_bitmaps),
    SIZE=836,
    )


def get():
    return senv_def

senv_def = TagDef("senv",
    blam_header('senv', 2),
    senv_body,

    ext=".shader_environment", endian=">", tag_cls=SenvTag
    )
