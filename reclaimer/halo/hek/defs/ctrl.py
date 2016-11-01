from .obje import *
from .devi import *
from supyr_struct.defs.tag_def import TagDef

ctrl_body = Struct("tagdata",
    object_attrs,
    devi_attrs,

    BSEnum16('type',
        'toggle switch',
        'on button',
        'off button',
        'call button'
        ),
    BSEnum16('triggers when',
        'touched by player',
        'destroyed'
        ),
    BFloat('call value', MIN=0.0, MAX=1.0),

    Pad(80),
    dependency("on", valid_event_effects),
    dependency("off", valid_event_effects),
    dependency("deny", valid_event_effects),

    SIZE=792,
    )


def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">"
    )
