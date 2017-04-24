from .obje import *
from .devi import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=9)

lifi_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,

    SIZE=720,
    )


def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">", tag_cls=HekTag
    )
