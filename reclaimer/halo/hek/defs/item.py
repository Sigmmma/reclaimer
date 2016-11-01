from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

item_attrs = Struct('item attrs',
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

    dependency("material effects", valid_material_effects),
    dependency("collision sound", valid_sounds),

    Pad(120),

    Struct("detonation delay", INCLUDE=from_to),
    dependency("detonating effect", valid_effects),
    dependency("detonation effect", valid_effects),
    SIZE=396,
    )

item_body = Struct('tagdata', item_attrs)

def get():
    return item_def

item_def = TagDef("item",
    blam_header('item', 2),
    item_body,

    ext=".item", endian=">"
    )
