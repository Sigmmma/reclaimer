from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from .objs.soso import SosoTag

os_soso_ext = Struct("shader model extension",
    #Specular Color
    TagIndexRef("specular color map", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("specular color coefficient"),
    Pad(4),
    BFloat("specular color exponent"),
    BBool16("flags",
        "alpha as exponent mask",
        ),
                     
    Pad(2),
    #Base Normal Map
    TagIndexRef("base normal map", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("base normal coefficient"),

    Pad(12),
    #Detail Normal Maps
    TagIndexRef("detail normal 1 map", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("detail normal 1 coefficient"),
    BFloat("detail normal 1 scale"),
    BFloat("detail normal 1 v-scale"),

    Pad(4),
    TagIndexRef("detail normal 2 map", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("detail normal 2 coefficient"),
    BFloat("detail normal 2 scale"),
    BFloat("detail normal 2 v-scale"),

    Pad(4),
    #Specular Tint Override
    BFloat("perpendicular brightness"),#[0,1]
    Struct("perpendicular tint color", INCLUDE=R_G_B_Float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color",      INCLUDE=R_G_B_Float),

    Pad(8),
    BFloat("specular Lighting exponent"),
    BFloat("specular Lighting coefficient"),
    SIZE=192,
    )


soso_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,
    
    #Shader Type
    Material_Type,
    Numeric_Shader_ID,

    Pad(2),
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
    BSEnum16("color change source", *Function_Names),
        
    Pad(30),
    #Self-Illumination
    Struct("self illumination",
        BBool16("flags",
            "no random phase"
            ),
        Pad(2),
        BSEnum16("color source", *Function_Names),
        BSEnum16("animation function", *Animation_Functions),
        BFloat("animation period"),#seconds
        Struct("color lower bound", INCLUDE=R_G_B_Float),
        Struct("color upper bound", INCLUDE=R_G_B_Float),
        ),
        
    Pad(12),
    #Diffuse, Multipurpose, and Detail Maps
    Struct("maps",
        BFloat("map u-scale"),
        BFloat("map v-scale"),
        TagIndexRef("diffuse map", INCLUDE=Tag_Index_Ref_Struct),
           
        Pad(8),
        TagIndexRef("multipurpose map", INCLUDE=Tag_Index_Ref_Struct),

        Pad(8),
        BSEnum16("detail function", *Detail_Map_Functions),
        BSEnum16("detail mask",     *Detail_Mask),
           
        BFloat("detail map scale"),
        TagIndexRef("detail map", INCLUDE=Tag_Index_Ref_Struct),
        BFloat("detail map v-scale"),
        ),
    
    #OS Shader Model Extension
    reflexive("os shader model ext", os_soso_ext, 1),
        
    #Texture Scrolling Animation
    Struct("texture scrolling",
        Struct("u-animation", INCLUDE=Anim_Src_Func_Per_Pha_Sca),
        Struct("v-animation", INCLUDE=Anim_Src_Func_Per_Pha_Sca),
        Struct("rotation-animation",   INCLUDE=Anim_Src_Func_Per_Pha_Sca),
        Struct("rot-animation center", INCLUDE=X_Y_Float),
        ),
                   
    Pad(8),
    #Reflection Properties
    Struct("reflection properties",
        BFloat("falloff distance"),#world units
        BFloat("cutoff distance"),#world units
     
        BFloat("perpendicular brightness"),#[0,1]
        Struct("perpendicular tint color", INCLUDE=R_G_B_Float),
        BFloat("parallel brightness"),#[0,1]
        Struct("parallel tint color",      INCLUDE=R_G_B_Float),

        TagIndexRef("reflection cube map map", INCLUDE=Tag_Index_Ref_Struct),
        ),
    SIZE=440,
    )


def get():
    return soso_def

soso_def = TagDef(
    blam_header('soso', 2),
    soso_body,
    
    NAME="shader_model",
    
    ext=".shader_model", def_id="soso", endian=">"
    )
