from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return SOUL_Def

class SOUL_Def(Tag_Def):

    Ext = ".ui_widget_collection"

    Cls_ID = "Soul"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"ui_widget_collection",
                     0:Combine( {1:{ DEFAULT:"Soul" } }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"UI Widget Definitions",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{TYPE:Array, GUI_NAME:"UI Widget Definitions",
                                    SIZE:".Count", MAX:32,
                                    SUB_STRUCT:{ TYPE:Tag_Index_Ref, SIZE:16,
                                                 GUI_NAME:"UI Widget Definition",
                                                 INCLUDE:Tag_Index_Ref_Struct,
                                                 }
                                    }
                             }
                         }
                     }
