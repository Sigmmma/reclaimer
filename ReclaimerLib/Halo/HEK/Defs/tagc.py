from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return TAGC_Def

class TAGC_Def(Tag_Def):

    Ext = ".tag_collection"

    Cls_ID = "tagc"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"tag_collection",
                     0:Combine( {1:{ DEFAULT:"tagc" } }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Tag References",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{TYPE:Array, GUI_NAME:"Tag References Array",
                                    SIZE:".Count", MAX:200,
                                    SUB_STRUCT:{ TYPE:Tag_Index_Ref,
                                                 SIZE:16, GUI_NAME:"Tag",
                                                 INCLUDE:Tag_Index_Ref_Struct,
                                                 }
                                    }
                             }
                         }
                     }
