from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

item_body = Struct("Data",
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

    BSEnum16("A in", *Device_Functions),
    BSEnum16("B in", *Device_Functions),
    BSEnum16("C in", *Device_Functions),
    BSEnum16("D in", *Device_Functions),

    Pad(164),

    TagIndexRef("material effects", INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("collision sound",  INCLUDE=Tag_Index_Ref_Struct),

    Pad(120),

    Struct("detonation delay", INCLUDE=From_To),
    TagIndexRef("detonating effect", INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("detonation effect", INCLUDE=Tag_Index_Ref_Struct),
    SIZE=396,
    )


def get():
    return item_def

item_def = TagDef(
    blam_header('item', 2),
    item_body,
    
    NAME="item",
    
    ext=".item", def_id="item", endian=">"
    )
