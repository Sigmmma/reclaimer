from .obje import *
from .devi import *
from supyr_struct.defs.tag_def import TagDef

lifi_body = Struct("tagdata",
    object_attrs,
    devi_attrs,

    SIZE=720,
    )


def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">"
    )
