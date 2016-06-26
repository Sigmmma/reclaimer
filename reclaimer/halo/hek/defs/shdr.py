from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

shader_body = Struct("tagdata",
    #Radiosity Properties
    radiosity_settings,

    #Shader Type
    material_type,
    FlSEnum16("numeric shader id", DEFAULT=-1,
              INCLUDE=shader_id_num),
    Pad(2),
    SIZE=40, 
    )


def get():
    return shdr_def

shdr_def = TagDef("shdr",
    blam_header('shdr'),
    shader_body,

    ext=".shader", endian=">"
    )
