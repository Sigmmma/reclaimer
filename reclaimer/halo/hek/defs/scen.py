from .obje import *
from supyr_struct.defs.tag_def import TagDef

scen_body = Struct("tagdata",
    obje_attrs,
    SIZE=508,
    )


def get():
    return scen_def

scen_def = TagDef("scen",
    blam_header('scen'),
    scen_body,

    ext=".scenery", endian=">"
    )
