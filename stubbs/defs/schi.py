from ...hek.defs.schi import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

schi_body = Struct("tagdata",
    shdr_attrs,
    schi_attrs,
    SIZE=108
    )
    
def get():
    return schi_def

schi_def = TagDef("schi",
    blam_header_stubbs('schi'),
    schi_body,

    ext=".shader_transparent_chicago", endian=">",
    )
