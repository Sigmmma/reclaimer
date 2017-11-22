from ...hek.defs.swat import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

swat_body = Struct("tagdata",
    shdr_attrs,
    swat_attrs,
    SIZE=320,
    )

def get():
    return swat_def

swat_def = TagDef("swat",
    blam_header_stubbs('swat', 2),
    swat_body,

    ext=".shader_transparent_water", endian=">"
    )
