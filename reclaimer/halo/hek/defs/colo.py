from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef


color = Struct("color",
    ascii_str32('name'),
    QStruct("color", INCLUDE=argb_float),
    SIZE=48,
    )

colo_body = Struct("tagdata",
    reflexive("colors", color, 512),
    SIZE=12
    )

def get():
    return colo_def

colo_def = TagDef("colo",
    blam_header('colo'),
    colo_body,

    ext=".color_table", endian=">"
    )
