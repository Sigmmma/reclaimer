from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return ColoDef

class ColoDef(TagDef):

    ext = ".color_table"

    tag_id = "colo"

    endian = ">"

    Color = { TYPE:Struct, SIZE:48, GUI_NAME:"Color",
              0:{ TYPE:StrLatin1, NAME:'Name', SIZE:32 },
              1:com({NAME:"Color"}, A_R_G_B_Float),
              }

    descriptor = {TYPE:Container, GUI_NAME:"color_table",
                     0:com( {1:{ DEFAULT:"colo" }}, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Colors",
                              INCLUDE:Reflexive_Struct,
                              CHILD:{ TYPE:Array, NAME:"Colors_Array",
                                      MAX:512, SIZE:".Count",
                                      SUB_STRUCT:Color
                                      }
                             }
                        }
                     }
