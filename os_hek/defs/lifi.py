from ...hek.defs.lifi import *

#import and use the open saucified obje attrs
from .obje import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=9)

lifi_body = dict(lifi_body)
lifi_body[0] = obje_attrs

def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">", tag_cls=HekTag
    )
