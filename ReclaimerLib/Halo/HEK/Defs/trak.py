from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return TRAK_Def

class TRAK_Def(Tag_Def):

    Ext = ".camera_track"

    Cls_ID = "trak"

    Endian = ">"

    Control_Point = { TYPE:Struct, SIZE:60, GUI_NAME:"Control Point",
                      0:Combine({NAME:"Position"}, I_J_K_Float),
                      1:Combine({NAME:"Orientation"}, I_J_K_W_Float),
                      }

    Tag_Structure = {TYPE:Container, GUI_NAME:"camera_track",
                     0:Combine( {1:{ DEFAULT:"trak" },
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
