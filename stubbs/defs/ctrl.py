from ...hek.defs.ctrl import *
from .obje import *
from .devi import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=8)

ctrl_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    ctrl_attrs,

    SIZE=792,
    )

def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header_stubbs('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">"
    )
