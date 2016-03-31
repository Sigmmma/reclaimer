from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return Str_Def

class Str_Def(TagDef):

    ext = ".string_list"

    def_id = "str#"

    endian = ">"

    string_data_struct = { TYPE:RawDataRef, SIZE:20, GUI_NAME:"String",
                           INCLUDE:Raw_Data_Ref_Struct,
                           CHILD:{TYPE:StrLatin1, NAME:"Raw_String_Data",
                                  SIZE:".Count"}
                           }
    
    descriptor = {TYPE:Container, GUI_NAME:"string_list",
                     0:com( {1:{ DEFAULT:"str#" } }, Tag_Header),                    
                     1:{TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                        0:{ TYPE:Reflexive, GUI_NAME:"Strings", OFFSET:0,
                            INCLUDE:Reflexive_Struct,
                            
                            CHILD:{TYPE:Array, NAME:"Strings_Array",
                                   MAX:32767, SIZE:".Count",
                                   SUB_STRUCT:string_data_struct
                                   }
                            }
                        }
                     }
