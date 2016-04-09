from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

sgla_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    Numeric_Shader_ID,

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
    Struct("background tint color", INCLUDE=R_G_B_Float),
    BFloat("background tint map scale"),
    TagIndexRef("background tint map", INCLUDE=Tag_Index_Ref_Struct),

    Pad(22),
    #Reflection Properties
    BSEnum16("reflection type",
        "bumped Cubemap",
        "flat Cubemap",
        "dynamic Mirror",
        ),
    BFloat("perpendicular brightness"),#[0,1]
    Struct("perpendicular tint color", INCLUDE=R_G_B_Float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color",      INCLUDE=R_G_B_Float),
    TagIndexRef("reflection map", INCLUDE=Tag_Index_Ref_Struct),

    BFloat("bump map scale"),
    TagIndexRef("bump map", INCLUDE=Tag_Index_Ref_Struct),

    Pad(132),
    #Diffuse Properties
    BFloat("diffuse map scale"),
    TagIndexRef("diffuse map", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("diffuse detail map scale"),
    TagIndexRef("diffuse detail map", INCLUDE=Tag_Index_Ref_Struct),

    Pad(32),
    #Specular Properties
    BFloat("specular map scale"),
    TagIndexRef("specular map", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("specular detail map scale"),
    TagIndexRef("specular detail map", INCLUDE=Tag_Index_Ref_Struct),

    SIZE=480,
    )


def get():
    return sgla_def

sgla_def = TagDef(
    com( {1:{DEFAULT:"sgla" }}, Tag_Header),
    sgla_body,
    
    NAME="shader_glass",
    
    ext=".shader_glass", def_id="sgla", endian=">"
    )
