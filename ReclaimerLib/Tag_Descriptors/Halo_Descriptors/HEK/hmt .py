from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return HMT_Definition

class HMT_Definition(Tag_Def):

    Ext = ".hud_message_text"

    Cls_ID = "hmt "

    Endianness = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"hud_message_text",
                     0:Combine( {1:{ DEFAULT:"hmt " } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:128, GUI_NAME:"Data",
                         0: {TYPE:Struct, OFFSET:0, GUI_NAME:"String" ,
                             ATTRIBUTES:Raw_Data_Reference_Structure,
                             CHILD:{TYPE:Str_Raw_UTF16, NAME:"Raw_String_Data",
                                    ENDIAN:'<', SIZE:".Byte_Count"}
                             },
                         1: {TYPE:Struct, OFFSET:20, GUI_NAME:"Message Elements" ,
                             ATTRIBUTES:Block_Reference_Structure,
                             CHILD:{TYPE:Array, NAME:"Message_Elements_Array", SIZE:".Block_Count",
                                    SUB_STRUCT:{ TYPE:Struct, SIZE:2, GUI_NAME:"Message Element",
                                                 0:{ TYPE:UInt8, OFFSET:0, GUI_NAME:"Type" },
                                                 1:{ TYPE:UInt8, OFFSET:1, GUI_NAME:"Data" }
                                                 }
                                    }
                             },
                         
                         2: {TYPE:Struct, OFFSET:32, GUI_NAME:"Messages" ,
                             ATTRIBUTES:Block_Reference_Structure,
                             CHILD:{TYPE:Array, NAME:"Messages_Array", SIZE:".Block_Count",
                                    SUB_STRUCT:{ TYPE:Struct, SIZE:64, GUI_NAME:"Message",
                                                 0:{ TYPE:Str_Latin1, OFFSET:0,
                                                     GUI_NAME:"Name", SIZE:32},
                                                 1:{ TYPE:UInt16, OFFSET:32, NAME:"Text_Start",
                                                     GUI_NAME:"Start Index Into Text Blob" },
                                                 2:{ TYPE:UInt16, OFFSET:34, NAME:"Message_Index",
                                                     GUI_NAME:"Start Index of Message Block" },
                                                 3:{ TYPE:UInt8, OFFSET:36,
                                                     GUI_NAME:"Panel Count" }
                                                 }
                                    }
                             }
                         }
                     }
