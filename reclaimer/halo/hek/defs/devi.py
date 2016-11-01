from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

devi_attrs = Struct("devi attrs",
    BBool32("flags",
        "position loops",
        "position not interpolated",
        ),

    BFloat("power transition time"),
    BFloat("power acceleration time"),
    BFloat("position transition time"),
    BFloat("position acceleration time"),
    BFloat("depowered position transition time"),
    BFloat("depowered position acceleration time"),

    BSEnum16("A in", *device_functions),
    BSEnum16("B in", *device_functions),
    BSEnum16("C in", *device_functions),
    BSEnum16("D in", *device_functions),

    dependency("open", valid_device_effects),
    dependency("close", valid_device_effects),
    dependency("opened", valid_device_effects),
    dependency("closed", valid_device_effects),
    dependency("depowered", valid_device_effects),
    dependency("repowered", valid_device_effects),

    BFloat("delay time"),
    Pad(8),
    dependency("delay effect", valid_device_effects),
    BFloat("automatic activation radius"),

    SIZE=276,
    )

devi_body = Struct('tagdata', devi_attrs)

def get():
    return devi_def

devi_def = TagDef("devi",
    blam_header('devi'),
    devi_body,

    ext=".device", endian=">"
    )
