from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

item_body = Struct("tagdata",
    Pad(2),
    BBool16("flags",
        "always maintains z up",
        "destroyed by explosions",
        "unaffected by gravity",
        ),

    BSInt16("message index"),
    BSInt16("sort order"),
    BFloat("scale"),
    BSInt16("hud message value scale"),

    Pad(18),

    BSEnum16("A in", *device_functions),
    BSEnum16("B in", *device_functions),
    BSEnum16("C in", *device_functions),
    BSEnum16("D in", *device_functions),

    Pad(164),

    dependency("material effects"),
    dependency("collision sound"),

    Pad(120),

    Struct("detonation delay", INCLUDE=from_to),
    dependency("detonating effect"),
    dependency("detonation effect"),
    SIZE=396,
    )


def get():
    return item_def

item_def = TagDef("item",
    blam_header('item', 2),
    item_body,

    ext=".item", endian=">"
    )
