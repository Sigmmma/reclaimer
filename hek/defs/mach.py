from .obje import *
from .devi import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=7)

mach_attrs = Struct("mach attrs",
    SEnum16('type',
        'door',
        'platform',
        'gear',
        ),
    Bool16('flags',
        'pathfinding obstable',
        'except when open',
        'elevator',
        ),
    float_sec('door open time'),  # seconds

    Pad(80),
    SEnum16('triggers when',
        'pause until crushed',
        'reverse directions'
        ),
    SInt16('elevator node')
    )

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

    ext=".device_machine", endian=">", tag_cls=HekTag
    )
