from ...hek.defs.sotr import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

sotr_body = Struct("tagdata",
    shdr_attrs,
    sotr_attrs,

    SIZE=108,
    )
    
def get():
    return sotr_def

sotr_def = TagDef("sotr",
    blam_header_stubbs("sotr"),
    sotr_body,

    ext=".shader_transparent_generic", endian=">",
    )
