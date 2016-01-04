from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return TAGC_Definition

class TAGC_Definition(Tag_Def):

    Ext = ".tag_collection"

    Cls_ID = "tagc"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"tag_collection",
                     0:Combine( {1:{ DEFAULT:"tagc" } }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Struct, GUI_NAME:"Tag References",
                             INCLUDE:Block_Reference_Structure,
                             
                             CHILD:{TYPE:Array, NAME:"Tag_Ref_Array",
                                    SIZE:".Block_Count", MAX:200,
                                    SUB_STRUCT:{ TYPE:Struct, SIZE:16, GUI_NAME:"Tag",
                                                 INCLUDE:Tag_Reference_Structure,
                                                 0:Com({ TYPE:Str_Latin1_Enum, GUI_NAME:"Tag Class", SIZE:4},
                                                       All_Tag_Enums)
                                                 }
                                    }
                             }
                         }
                     }
