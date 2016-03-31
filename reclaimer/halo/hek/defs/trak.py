from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return TrakDef

class TrakDef(TagDef):

    ext = ".camera_track"

    def_id = "trak"

    endian = ">"

    Control_Point = { TYPE:Struct, SIZE:60, GUI_NAME:"Control Point",
                      0:com({NAME:"Position"}, I_J_K_Float),
                      1:com({NAME:"Orientation"}, I_J_K_W_Float),
                      }

    descriptor = {TYPE:Container, GUI_NAME:"camera_track",
                     0:com( {1:{ DEFAULT:"trak" },
                                 5:{ DEFAULT:2}
                                 }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:48, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, OFFSET:4, GUI_NAME:"Control Points",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{ TYPE:Array, NAME:"Control Points Array",
                                     MAX:16, SIZE:".Count",
                                     SUB_STRUCT:Control_Point
                                     }
                             }
                        }
                     }
