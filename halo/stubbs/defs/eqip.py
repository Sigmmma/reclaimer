from ...hek.defs.eqip import *
from .obje import *
from .objs.tag import StubbsTag

eqip_attrs = dict(eqip_attrs)
eqip_attrs[1] = BSEnum16('grenade type', *grenade_types)

eqip_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    eqip_attrs,

    SIZE=944,
    )

def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">"
    )
