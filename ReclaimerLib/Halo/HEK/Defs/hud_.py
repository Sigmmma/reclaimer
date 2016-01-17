from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return HUD_Def

class HUD_Def(Tag_Def):

    Ext = ".hud_number"

    Cls_ID = "hud#"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"hud_number",
                     0:Combine( {1:{ DEFAULT:"hud#" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:100, GUI_NAME:"Data",
                         #I didnt feel like adding offsets since there is no
                         #padding until AFTER all entries. it's all sequential
                         0:{ TYPE:Tag_Index_Ref, GUI_NAME:"Digits Bitmap",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         1:{ TYPE:SInt8, GUI_NAME:"Bitmap Digit Width" },
                         2:{ TYPE:SInt8, GUI_NAME:"Screen Digit Width" },
                         3:{ TYPE:SInt8, GUI_NAME:"X Offset" },
                         4:{ TYPE:SInt8, GUI_NAME:"Y Offset" },
                         5:{ TYPE:SInt8, GUI_NAME:"Decimal Point Width" },
                         6:{ TYPE:SInt8, GUI_NAME:"Colon Width" },
                         }
                     }
