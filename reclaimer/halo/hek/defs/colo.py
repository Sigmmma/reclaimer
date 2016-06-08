from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


color = Struct("color",
    StrLatin1('name', SIZE=32),
    Struct("color", INCLUDE=A_R_G_B_Float),
    SIZE=48,
    )

colo_body = Struct("tagdata",
    reflexive("colors", color, 512),
    SIZE=12
    )

def get():
    return colo_def

colo_def = TagDef(
    blam_header('colo'),
    colo_body,
    
    NAME="color_table",
    
    ext=".color_table", def_id="colo", endian=">"
    )
