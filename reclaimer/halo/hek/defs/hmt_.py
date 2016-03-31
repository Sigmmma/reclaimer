from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return Hmt_Def

class Hmt_Def(TagDef):

    ext = ".hud_message_text"

    def_id = "hmt "

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"hud_message_text",
                     0:com( {1:{ DEFAULT:"hmt " } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:128, GUI_NAME:"Data",
                         0: {TYPE:RawDataRef, OFFSET:0, GUI_NAME:"String" ,
                             INCLUDE:Raw_Data_Ref_Struct,
                             CHILD:{TYPE:FlUTF16StrData,
                                    GUI_NAME:"Raw String Data", SIZE:".Count"}
                             },
                         1: {TYPE:Reflexive, OFFSET:20, GUI_NAME:"Message Elements" ,
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, GUI_NAME:"Message Elements Array", SIZE:".Count",
                                    SUB_STRUCT:{ TYPE:Struct, SIZE:2, GUI_NAME:"Message Element",
                                                 0:{ TYPE:SInt8, OFFSET:0, GUI_NAME:"Type" },
                                                 1:{ TYPE:SInt8, OFFSET:1, GUI_NAME:"Data" }
                                                 }
                                    }
                             },
                         
                         2: {TYPE:Reflexive, OFFSET:32, GUI_NAME:"Messages" ,
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, GUI_NAME:"Messages Array", SIZE:".Count",
                                    SUB_STRUCT:{ TYPE:Struct, SIZE:64, GUI_NAME:"Message",
                                                 0:{ TYPE:StrLatin1, OFFSET:0,
                                                     GUI_NAME:"Name", SIZE:32},
                                                 1:{ TYPE:SInt16, OFFSET:32, NAME:"Text Start",
                                                     GUI_NAME:"Start Index Into Text Blob" },
                                                 2:{ TYPE:SInt16, OFFSET:34, NAME:"Message Index",
                                                     GUI_NAME:"Start Index of Message Block" },
                                                 3:{ TYPE:SInt8, OFFSET:36,
                                                     GUI_NAME:"Panel Count" }
                                                 }
                                    }
                             }
                         }
                     }
