from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from .objs.senv import SenvTag

senv_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    FlSEnum16("numeric shader id", DEFAULT=3,
              INCLUDE=Numeric_Shader_ID),
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
    TagIndexRef("lens flare", INCLUDE=Tag_Index_Ref_Struct),
    Pad(44),

    #Diffuse Properties
    BBool16("diffuse flags" ,
        "rescale detail maps",
        "rescale bump maps",
        ),
    Pad(26),
    TagIndexRef("base map", INCLUDE=Tag_Index_Ref_Struct),
                   
    Pad(24),
    BSEnum16(   "detail map function", *Detail_Map_Functions),
    Pad(2),
    BFloat(     "primary detail map scale"),
    TagIndexRef("primary detail map",   INCLUDE=Tag_Index_Ref_Struct),
    BFloat(     "secondary detail map scale"),
    TagIndexRef("secondary detail map", INCLUDE=Tag_Index_Ref_Struct),
    Pad(24),
    BSEnum16(   "micro detail map function", *Detail_Map_Functions),
    Pad(2),
    BFloat(     "micro detail map scale"),
    TagIndexRef("micro detail map",     INCLUDE=Tag_Index_Ref_Struct),
                   
    Struct("material color", INCLUDE=R_G_B_Float),

    Pad(12),
    #Bump Properties
    BFloat("bump map scale"),
    TagIndexRef("bump map", INCLUDE=Tag_Index_Ref_Struct),
    FlFloat("bump map scale x"),
    FlFloat("bump map scale y"),

    Pad(16),
    #Texture Animation
    Struct("u-animation", INCLUDE=Anim_Func_Per_Sca),
    Struct("V-animation", INCLUDE=Anim_Func_Per_Sca),

    Pad(52),
    #Self Illumination
    Struct("primary on-color",  INCLUDE=R_G_B_Float),
    Struct("primary off-color", INCLUDE=R_G_B_Float),
    Struct("primary animation", INCLUDE=Anim_Func_Per_Pha),

    Pad(24),
    Struct("secondary on-color",  INCLUDE=R_G_B_Float),
    Struct("secondary off-color", INCLUDE=R_G_B_Float),
    Struct("secondary animation", INCLUDE=Anim_Func_Per_Pha),

    Pad(24),
    Struct("plasma on-color",  INCLUDE=R_G_B_Float),
    Struct("plasma off-color", INCLUDE=R_G_B_Float),
    Struct("plasma animation", INCLUDE=Anim_Func_Per_Pha),

    Pad(24),
    BFloat("illumination map scale"),
    TagIndexRef("illumination map", INCLUDE=Tag_Index_Ref_Struct),

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
    Struct("perpendicular color", INCLUDE=R_G_B_Float),
    Struct("parallel color",      INCLUDE=R_G_B_Float),

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
    TagIndexRef("reflection cube map", INCLUDE=Tag_Index_Ref_Struct),
    SIZE=836,
    )


def get():
    return senv_def

senv_def = TagDef(
    com( {1:{DEFAULT:"senv" },
          5:{DEFAULT:2}}, Tag_Header),
    senv_body,
    
    NAME="shader_environment",
    
    ext=".shader_environment", def_id="senv", endian=">", tag_cls=SenvTag
    )
