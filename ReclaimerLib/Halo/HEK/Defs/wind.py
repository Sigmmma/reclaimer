from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return WIND_Def

class WIND_Def(Tag_Def):

    Ext = ".wind"

    Cls_ID = "wind"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"wind",
                     0:Combine( {1:{ DEFAULT:"wind" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:64, GUI_NAME:"Data",
                        #I didnt feel like adding offsets since there is no
                        #padding until AFTER all entries. it's all sequential
                        0:Com({ GUI_NAME:"Velocity" }, From_To),
                        1:Com({ GUI_NAME:"Variation Area" }, Y_P_Float),
                        2:{ TYPE:Float, GUI_NAME:"Local Variation Weight" },
                        3:{ TYPE:Float, GUI_NAME:"Local Variation Rate" },
                        4:{ TYPE:Float, GUI_NAME:"Damping" }
                        }
                     }
