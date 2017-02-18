from ...hek.defs.lifi import *

#import and use the open saucified obje attrs
from .obje import *

lifi_body = dict(lifi_body)
lifi_body[0] = obje_attrs

def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">"
    )
