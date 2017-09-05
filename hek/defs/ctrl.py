from .obje import *
from .devi import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=8)

ctrl_attrs = Struct("ctrl attrs",
    SEnum16('type',
        'toggle switch',
        'on button',
        'off button',
        'call button'
        ),
    SEnum16('triggers when',
        'touched by player',
        'destroyed'
        ),
    float_zero_to_one('call value'),

    Pad(80),
    dependency("on", valid_event_effects),
    dependency("off", valid_event_effects),
    dependency("deny", valid_event_effects),
    )

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

    ext=".device_control", endian=">", tag_cls=HekTag
    )
