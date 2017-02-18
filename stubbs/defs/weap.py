from ...hek.defs.weap import *
from .obje import *
from .item import *

# replace the object_type enum one that uses
# the correct default value for this object
weap_attrs = dict(weap_attrs)
weap_attrs[24] = BSEnum16('weapon type', *weapon_types)

weap_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    weap_attrs,
    SIZE=1288,
    )

def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">"
    )
