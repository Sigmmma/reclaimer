from ...os_v3_hek.defs.vehi import *

#import and use the open saucified obje and unit attrs
from .obje import *
from .unit import *

vehi_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    vehi_attrs,
    SIZE=1008,
    )


def get():
    return vehi_def

vehi_def = TagDef("vehi",
    blam_header('vehi'),
    vehi_body,

    ext=".vehicle", endian=">"
    )
