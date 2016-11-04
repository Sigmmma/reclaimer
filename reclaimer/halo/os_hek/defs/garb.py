from ...hek.defs.garb import *

#import and use the open saucified obje attrs
from .obje import *

garb_body = dict(garb_body)
garb_body[0] = obje_attrs


def get():
    return garb_def

garb_def = TagDef("grab",
    blam_header('garb'),
    garb_body,

    ext=".garbage", endian=">"
    )
