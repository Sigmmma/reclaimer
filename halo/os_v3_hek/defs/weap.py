from ...hek.defs.weap import *

#import and use the open saucified obje attrs
from .obje import *

weap_body = dict(weap_body)
weap_body[0] = obje_attrs

def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">"
    )
