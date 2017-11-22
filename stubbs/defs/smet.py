from ...hek.defs.smet import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

smet_body = Struct("tagdata",
    shdr_attrs,
    smet_attrs,
    SIZE=260,
    )

def get():
    return smet_def

smet_def = TagDef("smet",
    blam_header_stubbs('smet'),
    smet_body,

    ext=".shader_transparent_meter", endian=">"
    )
