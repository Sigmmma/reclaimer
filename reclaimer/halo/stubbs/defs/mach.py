from ...hek.defs.mach import *
from .obje import *
from .devi import *
from .objs.tag import StubbsTag
from supyr_struct.defs.tag_def import TagDef

mach_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    mach_attrs,

    SIZE=804,
    )

def get():
    return mach_def

mach_def = TagDef("mach",
    blam_header('mach'),
    mach_body,

    ext=".device_machine", endian=">"
    )
