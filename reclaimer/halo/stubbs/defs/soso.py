from ...hek.defs.soso import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

soso_body = Struct("tagdata",
    shdr_attrs,
    soso_attrs,
    SIZE=440
    )

def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header('soso', 2),
    soso_body,

    ext=".shader_model", endian=">"
    )
