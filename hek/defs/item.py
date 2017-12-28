from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

message_index_comment = """MESSAGE INDEX
This sets which string from tags\\ui\\hud\\hud_item_messages.unicode_string_list to display."""

item_attrs = Struct('item attrs',
    Bool32("flags",
        "always maintains z up",
        "destroyed by explosions",
        "unaffected by gravity",
        ),
    SInt16("message index", COMMENT=message_index_comment),
    SInt16("sort order"),
    Float("scale"),
    SInt16("hud message value scale"),

    Pad(18),

    SEnum16("A in", *device_functions),
    SEnum16("B in", *device_functions),
    SEnum16("C in", *device_functions),
    SEnum16("D in", *device_functions),

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
