from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return UstrDef

class UstrDef(TagDef):

    ext = ".unicode_string_list"

    tag_id = "ustr"

    endian = ">"

    string_data_struct = { TYPE:RawDataRef, SIZE:20, GUI_NAME:"String",
                           INCLUDE:Raw_Data_Ref_Struct,
                           CHILD:{ TYPE:FlStrUTF16, NAME:"Raw_String_Data",
                                   SIZE:".Count" }
                           }
    
    descriptor = {TYPE:Container, GUI_NAME:"unicode_string_list",
                     0:com( {1:{ DEFAULT:"ustr" } }, Tag_Header),                    
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
