#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .devi import *
from .objs.mach import MachTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=7)

mach_attrs = Struct("mach_attrs",
    SEnum16('type',
        'door',
        'platform',
        'gear',
        ),
    Bool16('flags',
        'pathfinding_obstable',
        'except_when_open',
        'elevator',
        ),
    float_sec('door_open_time'),  # seconds

    Pad(80),
    SEnum16('triggers_when',
        'pause_until_crushed',
        'reverse_directions'
        ),
    SInt16('elevator_node'),
    Pad(52),
    UInt32("door_open_time_ticks")
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

    ext=".device_machine", endian=">", tag_cls=MachTag
    )
