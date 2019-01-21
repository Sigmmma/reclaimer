from ...hek.defs.eqip import *
from .obje import *
from ..common_descs import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=3)

eqip_attrs = dict(eqip_attrs)
eqip_attrs[1] = SEnum16('grenade type', *grenade_types)

eqip_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    eqip_attrs,

    SIZE=944,
    )

def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header_stubbs('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">"
    )
