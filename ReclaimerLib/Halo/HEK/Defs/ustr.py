from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return USTR_Def

class USTR_Def(Tag_Def):

    Ext = ".unicode_string_list"

    Cls_ID = "ustr"

    Endian = ">"
    
    Tag_Structure = {TYPE:Container, GUI_NAME:"unicode_string_list",
                     0:Combine( {1:{ DEFAULT:"ustr" } }, Tag_Header),                    
                     1:{TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                        0:{ TYPE:Reflexive, GUI_NAME:"Strings", OFFSET:0,
                            INCLUDE:Reflexive_Struct,
                            
                            CHILD:{TYPE:Array, NAME:"Strings_Array",
                                   MAX:32767, SIZE:".Count",
                                   SUB_STRUCT:{ TYPE:Raw_Data_Ref,
                                                SIZE:20, GUI_NAME:"String",
                                                INCLUDE:Raw_Data_Ref_Struct,
                                                CHILD:{TYPE:FL_Str_UTF16, SIZE:".Count",
                                                       NAME:"Raw_String_Data" }
                                                }
                                   }
                            }
                        }
                     }
