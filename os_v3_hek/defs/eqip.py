from ...hek.defs.eqip import *

#import and use the open saucified obje attrs
from .obje import *

eqip_body = dict(eqip_body)
eqip_body[0] = obje_attrs

def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">"
    )
