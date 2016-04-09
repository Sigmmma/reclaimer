from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

smet_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    FlSEnum16("numeric shader id", DEFAULT=10,
              INCLUDE=Numeric_Shader_ID),

    Pad(2),
    #Meter Shader Properties
    BBool16("meter shader flags",
        "decal",
        "two-sided",
        "flash color is negative",
        "tint mode-2",
        "unfiltered"
        ),
    Pad(34),
    TagIndexRef("meter map", INCLUDE=Tag_Index_Ref_Struct),
    Pad(32),

    #Colors
    Struct("gadient min color", INCLUDE=R_G_B_Float),
    Struct("gadient max color", INCLUDE=R_G_B_Float),
    Struct("background color", INCLUDE=R_G_B_Float),
    Struct("flash color", INCLUDE=R_G_B_Float),
    Struct("tint color", INCLUDE=R_G_B_Float),
    BFloat("meter transparency"),
    BFloat("background transparency"),
    Pad(24),

    #External Function Sources
    BSEnum16("meter brightness source", *Function_Outputs),
    BSEnum16("flash brightness source", *Function_Outputs),
    BSEnum16("value source",            *Function_Outputs),
    BSEnum16("gradient source",         *Function_Outputs),
    BSEnum16("flash-extension source",  *Function_Outputs),
    SIZE=260,
    )



def get():
    return smet_def

smet_def = TagDef(
    blam_header('smet'),
    smet_body,
    
    NAME="shader_meter",
    
    ext=".shader_meter", def_id="smet", endian=">"
    )
