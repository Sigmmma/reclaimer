from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

item_attrs = Struct('item attrs',
    BBool32("flags",
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

    dependency("material effects", "foot"),
    dependency("collision sound", "snd!"),

    Pad(120),

    from_to_sec("detonation delay"),
    dependency("detonating effect", "effe"),
    dependency("detonation effect", "effe"),
    SIZE=396,
    )

item_body = Struct('tagdata',
    item_attrs,
    SIZE=396
    )

def get():
    return item_def

item_def = TagDef("item",
    blam_header('item', 2),
    item_body,

    ext=".item", endian=">", tag_cls=HekTag
    )
