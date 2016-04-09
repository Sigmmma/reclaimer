from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


spla_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    FlSEnum16("numeric shader id", DEFAULT=11,
              INCLUDE=Numeric_Shader_ID),

    Pad(6),
    #Intensity
    BSEnum16("intensity source", *Function_Outputs),
    Pad(2),
    BFloat("intensity exponent"),

    #Offset
    BSEnum16("offset source", *Function_Outputs),
    Pad(2),
    BFloat("offset amount"),
    BFloat("offset exponent"),

    Pad(32),

    #Color
    BFloat("perpendicular brightness"),#[0,1]
    Struct("perpendicular tint color", INCLUDE=R_G_B_Float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color", INCLUDE=R_G_B_Float),
    BSEnum16("tint color source", *Function_Names),

    Pad(62),
    #Primary Noise Map
    BFloat("primary animation period"),
    Struct("primary animation direction", INCLUDE=I_J_K_Float),
    BFloat("primary noise map scale"),
    TagIndexRef("primary noise map", INCLUDE=Tag_Index_Ref_Struct),

    Pad(36),
    #Secondary Noise Map
    BFloat("secondary animation period"),
    Struct("secondary animation direction", INCLUDE=I_J_K_Float),
    BFloat("secondary noise map scale"),
    TagIndexRef("secondary noise map", INCLUDE=Tag_Index_Ref_Struct),
    SIZE=332,
    )


def get():
    return spla_def

spla_def = TagDef(
    com( {1:{DEFAULT:"spla" }}, Tag_Header),
    spla_body,
    
    NAME="shader_transparent_plasma",
    
    ext=".shader_transparent_plasma", def_id="spla", endian=">"
    )
