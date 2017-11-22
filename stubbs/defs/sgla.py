from ...hek.defs.sgla import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

sgla_body = Struct("tagdata",
    shdr_attrs,
    sgla_attrs,
    SIZE=480,
    )

def get():
    return sgla_def

sgla_def = TagDef("sgla",
    blam_header_stubbs('sgla'),
    sgla_body,

    ext=".shader_transparent_glass", endian=">"
    )
