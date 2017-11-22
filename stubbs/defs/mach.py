from ...hek.defs.mach import *
from .obje import *
from .devi import *
from .objs.tag import StubbsTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=7)

mach_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    mach_attrs,

    SIZE=804,
    )

def get():
    return mach_def

mach_def = TagDef("mach",
    blam_header_stubbs('mach'),
    mach_body,

    ext=".device_machine", endian=">"
    )
