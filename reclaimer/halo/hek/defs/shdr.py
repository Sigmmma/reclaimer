from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

shader_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    Numeric_Shader_ID,
    SIZE=40, 
    )


def get():
    return shdr_def

shdr_def = TagDef(
    com( {1:{DEFAULT:"shdr" }}, Tag_Header),
    shader_body,
    
    NAME="shader",
    
    ext=".shader", def_id="shdr", endian=">"
    )
