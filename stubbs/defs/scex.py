from ...hek.defs.scex import *
from .schi import *
from supyr_struct.defs.tag_def import TagDef

scex_body = Struct("tagdata",
    shdr_attrs,
    scex_attrs,
    SIZE=120
    )

def get():
    return scex_def

scex_def = TagDef("scex",
    blam_header_stubbs('scex'),
    scex_body,

    ext=".shader_transparent_chicago_extended", endian=">"
    )
