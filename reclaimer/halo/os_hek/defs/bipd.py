from ...hek.defs.bipd import *

#import and use the open saucified obje and unit attrs
from .obje import *
from .unit import *

bipd_body = dict(bipd_body)
bipd_body[0] = obje_attrs
bipd_body[1] = unit_attrs


def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">"
    )
