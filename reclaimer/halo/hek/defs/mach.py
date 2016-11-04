from .obje import *
from .devi import *
from supyr_struct.defs.tag_def import TagDef

mach_attrs = Struct("mach attrs",
    BSEnum16('type',
        'door',
        'platform',
        'gear',
        ),
    BBool16('flags',
        'pathfinding obstable',
        'except when open',
        'elevator',
        ),
    BFloat('door open time'),  # seconds

    Pad(80),
    BSEnum16('triggers when',
        'pause until crushed',
        'reverse directions'
        ),
    BSInt16('elevator node')
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

    ext=".device_machine", endian=">"
    )
