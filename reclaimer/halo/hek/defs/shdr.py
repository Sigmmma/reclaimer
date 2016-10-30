from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

shader_body = Struct("tagdata",
    radiosity_settings,
    shader_physics,
    SIZE=40, 
    )


def get():
    return shdr_def

shdr_def = TagDef("shdr",
    blam_header('shdr'),
    shader_body,

    ext=".shader", endian=">"
    )
