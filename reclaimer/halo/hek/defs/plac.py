from .obje import *
from supyr_struct.defs.tag_def import TagDef

plac_body = Struct("tagdata",
    obje_attrs,
    SIZE=508,
    )


def get():
    return plac_def

plac_def = TagDef("plac",
    blam_header('plac', 2),
    plac_body,

    ext=".placeholder", endian=">"
    )
