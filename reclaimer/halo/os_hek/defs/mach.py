from ...hek.defs.mach import *

#import and use the open saucified obje attrs
from .obje import *

mach_body = dict(mach_body)
mach_body[0] = obje_attrs

def get():
    return mach_def

mach_def = TagDef("mach",
    blam_header('mach'),
    mach_body,

    ext=".device_machine", endian=">"
    )
