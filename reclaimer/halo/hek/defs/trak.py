from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


control_point = Struct("control point",
    Struct("position", I_J_K_Float),
    Struct("orientation", I_J_K_W_Float),
    SIZE=60,
    )

trak_body = Struct("Data",
    Pad(4),
    Reflexive("control points",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("control points array",
            MAX=16, SIZE=".Count",
            SUB_STRUCT=control_point,
            ),
        ),
    SIZE=48,
    )


def get():
    return trak_def

trak_def = TagDef(
    com( {1:{DEFAULT:"trak" },
          5:{DEFAULT:2}}, Tag_Header),
    trak_body,
    
    NAME="camera_track",
    
    ext=".camera_track", def_id="trak", endian=">"
    )
