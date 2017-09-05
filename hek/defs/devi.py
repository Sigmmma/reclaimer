from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

devi_attrs = Struct("devi attrs",
    Bool32("flags",
        "position loops",
        "position not interpolated",
        ),

    float_sec("power transition time"),
    float_sec("power acceleration time"),
    float_sec("position transition time"),
    float_sec("position acceleration time"),
    float_sec("depowered position transition time"),
    float_sec("depowered position acceleration time"),

    SEnum16("A in", *device_functions),
    SEnum16("B in", *device_functions),
    SEnum16("C in", *device_functions),
    SEnum16("D in", *device_functions),

    dependency("open", valid_event_effects),
    dependency("close", valid_event_effects),
    dependency("opened", valid_event_effects),
    dependency("closed", valid_event_effects),
    dependency("depowered", valid_event_effects),
    dependency("repowered", valid_event_effects),

    float_sec("delay time"),
    Pad(8),
    dependency("delay effect", valid_event_effects),
    float_wu("automatic activation radius"),

    SIZE=276,
    )

devi_body = Struct('tagdata',
    devi_attrs,
    SIZE=276
    )

def get():
    return devi_def

devi_def = TagDef("devi",
    blam_header('devi'),
    devi_body,

    ext=".device", endian=">", tag_cls=HekTag
    )
