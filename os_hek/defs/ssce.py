from ...hek.defs.ssce import *

#import and use the open saucified obje attrs
from .obje import *

ssce_body = dict(ssce_body)
ssce_body[0] = obje_attrs

def get():
    return ssce_def

ssce_def = TagDef("ssce",
    blam_header('ssce'),
    ssce_body,

    ext=".sound_scenery", endian=">"
    )
