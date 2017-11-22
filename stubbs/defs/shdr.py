from ...hek.defs.shdr import *
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

shdr_attrs = dict(shdr_attrs)
shdr_attrs[6] = SEnum16("material type", *materials_list)

shader_body = Struct("tagdata",
    shdr_attrs,
    SIZE=40
    )

def get():
    return shdr_def

shdr_def = TagDef("shdr",
    blam_header_stubbs('shdr'),
    shader_body,

    ext=".shader", endian=">"
    )
