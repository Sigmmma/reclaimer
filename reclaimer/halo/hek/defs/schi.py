from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from .objs.schi import SchiTag

schi_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    FlSEnum16("numeric shader id", DEFAULT=6,
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
    reflexive("extra layers", Extra_Layers_Block, 4),
    reflexive("maps", Chicago_4_Stage_Maps, 4),
    BBool32("extra flags", *Chicago_Extra_Flags),
    SIZE=108,
    )

    
def get():
    return schi_def

schi_def = TagDef(
    blam_header('schi'),
    schi_body,
    
    NAME="shader_transparent_chicago",
    
    ext=".shader_transparent_chicago",
    def_id="schi", endian=">", tag_cls=SchiTag
    )
