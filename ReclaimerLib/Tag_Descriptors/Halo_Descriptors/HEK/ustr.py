from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return USTR_Definition

class USTR_Definition(Tag_Def):

    Tag_Ext = ".unicode_string_list"

    Cls_ID = "ustr"

    Endianness = ">"
    
    Tag_Structure = {TYPE:Container, GUI_NAME:"unicode_string_list",
                     0:Combine( {1:{ DEFAULT:"ustr" } }, Tag_Header),                    
                     1:{TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                        0:{ TYPE:Struct, GUI_NAME:"Strings", OFFSET:0,
                            ATTRIBUTES:Block_Reference_Structure,
                            
                            CHILD:{TYPE:Array, NAME:"Strings_Array",
                                   MAX:32767, SIZE:".Block_Count",
                                   ARRAY_ELEMENT:{TYPE:Struct, SIZE:20, GUI_NAME:"String",
                                                  ATTRIBUTES:Raw_Data_Reference_Structure,
                                                  CHILD:{TYPE:Str_Raw_UTF16, NAME:"Raw_String_Data",
                                                         ENDIAN:'<', SIZE:".Byte_Count"}
                                                  }
                                   }
                            }
                        }
                     }
