from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return HMT_Def

class HMT_Def(Tag_Def):

    Ext = ".hud_message_text"

    Cls_ID = "hmt "

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"hud_message_text",
                     0:Combine( {1:{ DEFAULT:"hmt " } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:128, GUI_NAME:"Data",
                         0: {TYPE:Raw_Data_Ref, OFFSET:0, GUI_NAME:"String" ,
                             INCLUDE:Raw_Data_Ref_Struct,
                             CHILD:{TYPE:FL_UTF16_Str_Data,
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
                                                 0:{ TYPE:Str_Latin1, OFFSET:0,
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
