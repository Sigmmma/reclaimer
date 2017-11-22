from ...hek.defs.ctrl import *
from .obje import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=8)

ctrl_body = dict(ctrl_body)
ctrl_body[0] = obje_attrs

def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">", tag_cls=HekTag
    )
