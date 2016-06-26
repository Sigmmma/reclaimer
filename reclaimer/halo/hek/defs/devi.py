from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

devi_body = Struct("tagdata",
    Pad(2),
    BBool16("flags",
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
                   
    dependency("open"),
    dependency("close"),
    dependency("opened"),
    dependency("closed"),
    dependency("depowered"),
    dependency("repowered"),
    
    BFloat("delay time"),
    Pad(8),
    dependency("delay effect"),
    BFloat("automatic activation radius"),
                   
    SIZE=276,
    )


def get():
    return devi_def

devi_def = TagDef("devi",
    blam_header('devi'),
    devi_body,

    ext=".device", endian=">"
    )
