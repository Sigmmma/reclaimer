from ...hek.defs.bipd import *

#import and use the open saucified obje and unit attrs
from .obje import *
from .unit import *

bipd_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    bipd_attrs,
    SIZE=1268,
    )

def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">"
    )
