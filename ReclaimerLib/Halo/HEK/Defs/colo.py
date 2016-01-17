from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return COLO_Def

class COLO_Def(Tag_Def):

    Ext = ".color_table"

    Cls_ID = "colo"

    Endian = ">"

    Color = { TYPE:Struct, SIZE:48, GUI_NAME:"Color",
              0:{ TYPE:Str_Latin1, NAME:'Name', SIZE:32 },
              1:Combine({NAME:"Color"}, A_R_G_B_Float),
              }

    Tag_Structure = {TYPE:Container, GUI_NAME:"color_table",
                     0:Combine( {1:{ DEFAULT:"colo" }}, Tag_Header),
                     
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
