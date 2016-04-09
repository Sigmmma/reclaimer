from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from .objs.scex import ScexTag

scex_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    FlSEnum16("numeric shader id", DEFAULT=7,
              INCLUDE=Numeric_Shader_ID),
    Pad(2),

    # Shader Properties
    SInt8("numeric counter limit"),#[0,255]

    Bool8("chicago shader flags",          *Transparent_Shader_Properties),
    BSEnum16("first map type",             *Transparent_Shader_First_Map_Type),
    BSEnum16("framebuffer blend function", *Framebuffer_Blend_Modes),
    BSEnum16("framebuffer fade mode",      *Transparent_Shader_Fade_Mode),
    BSEnum16("framebuffer fade source",    *Function_Outputs),

    Pad(2),

    #Lens Flare
    BFloat("lens flare spacing"),#world units
    TagIndexRef("lens flare", INCLUDE=Tag_Index_Ref_Struct),

    Reflexive("extra layers", INCLUDE=Reflexive_Struct,
        CHILD=Array("extra layers array",
            MAX=4, SIZE=".Count",
            SUB_STRUCT=Extra_Layers_Block ),
        ),

    Reflexive("four stage maps", INCLUDE=Reflexive_Struct,
        CHILD=Array("four stage maps array",
            MAX=4, SIZE=".Count",
            SUB_STRUCT=Chicago_4_Stage_Maps ),
        ),
    Reflexive("two stage maps", INCLUDE=Reflexive_Struct,
        CHILD=Array("two stage maps array",
            MAX=2, SIZE=".Count",
            SUB_STRUCT=Chicago_2_Stage_Maps ),
        ),
    BBool32("extra flags", *Chicago_Extra_Flags),
    SIZE=120,
    )


def get():
    return scex_def

scex_def = TagDef(
    com( {1:{DEFAULT:"scex" }}, Tag_Header),
    scex_body,
    
    NAME="shader_transparent_chicago_extended",
    
    ext=".shader_transparent_chicago_extended", 
    def_id="scex", endian=">", tag_cls=ScexTag
    )
