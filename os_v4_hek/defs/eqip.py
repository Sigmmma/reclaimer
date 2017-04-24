from ...os_v3_hek.defs.eqip import *

#import and use the open saucified obje attrs
from .obje import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=3)

eqip_body = dict(eqip_body)
eqip_body[0] = obje_attrs

def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">", tag_cls=HekTag
    )
