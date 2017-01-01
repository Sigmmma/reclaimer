from ...hek.defs.vehi import *
from .obje import *
from .unit import *

vehi_attrs = dict(vehi_attrs)
vehi_attrs[1] = BSEnum16('type', *vehicle_types)

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
