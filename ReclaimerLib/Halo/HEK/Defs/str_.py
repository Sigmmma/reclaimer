from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return STR_Def

class STR_Def(Tag_Def):

    Ext = ".string_list"

    Cls_ID = "str#"

    Endian = ">"
    
    Tag_Structure = {TYPE:Container, GUI_NAME:"string_list",
                     0:Combine( {1:{ DEFAULT:"str#" } }, Tag_Header),                    
                     1:{TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                        0:{ TYPE:Reflexive, GUI_NAME:"Strings", OFFSET:0,
                            INCLUDE:Reflexive_Struct,
                            
                            CHILD:{TYPE:Array, NAME:"Strings_Array",
                                   MAX:32767, SIZE:".Count",
                                   SUB_STRUCT:{ TYPE:Raw_Data_Ref, SIZE:20, GUI_NAME:"String",
                                                INCLUDE:Raw_Data_Ref_Struct,
                                                CHILD:{TYPE:Str_Latin1, NAME:"Raw_String_Data",
                                                       SIZE:".Count"}
                                                }
                                   }
                            }
                        }
                     }
