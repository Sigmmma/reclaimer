from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


color = Struct("color",
    StrLatin1('name', SIZE=32),
    Struct("color", INCLUDE=A_R_G_B_Float),
    SIZE=48,
    )

colo_body = Struct("Data",
    Reflexive("colors",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("colors_array",
            MAX=512, SIZE=".Count",
            SUB_STRUCT=color,
            )
        ),
    SIZE=12
    )

def get():
    return colo_def

colo_def = TagDef(
    com( {1:{DEFAULT:"colo" }}, Tag_Header),
    colo_body,
    
    NAME="color_table",
    
    ext=".color_table", def_id="colo", endian=">"
    )
