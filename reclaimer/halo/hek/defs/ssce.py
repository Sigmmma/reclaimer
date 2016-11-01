from .obje import *
from supyr_struct.defs.tag_def import TagDef

ssce_body = Struct("tagdata",
    object_attrs,
    SIZE=508,
    )


def get():
    return ssce_def

ssce_def = TagDef("ssce",
    blam_header('ssce'),
    ssce_body,

    ext=".sound_scenery", endian=">"
    )
