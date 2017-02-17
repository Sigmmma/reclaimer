from ...hek.defs.plac import *

#import and use the open saucified obje attrs
from .obje import *

plac_body = dict(plac_body)
plac_body[0] = obje_attrs

def get():
    return plac_def

plac_def = TagDef("plac",
    blam_header('plac', 2),
    plac_body,

    ext=".placeholder", endian=">"
    )
