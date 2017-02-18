from ...hek.defs.scen import *

#import and use the open saucified obje attrs
from .obje import *

scen_body = dict(scen_body)
scen_body[0] = obje_attrs

def get():
    return scen_def

scen_def = TagDef("scen",
    blam_header('scen'),
    scen_body,

    ext=".scenery", endian=">"
    )
