from ...hek.defs.ctrl import *
from .obje import *
from .devi import *
from .objs.tag import StubbsTag

ctrl_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    ctrl_attrs,

    SIZE=792,
    )

def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">"
    )
