from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

ngpr_body = Struct("tagdata",
    ascii_str32("name"),
    QStruct("primary color",   INCLUDE=rgb_float),
    QStruct("secondary color", INCLUDE=rgb_float),

    dependency("pattern", valid_bitmaps),
    BSInt16("pattern bitmap index"),
    Pad(2),
    dependency("decal", valid_bitmaps),
    BSInt16("decal bitmap index"),
    SIZE=896
    )


def get():
    return ngpr_def

ngpr_def = TagDef("ngpr",
    blam_header('ngpr', 2),
    ngpr_body,

    ext=".preferences_network_game", endian=">"
    )
