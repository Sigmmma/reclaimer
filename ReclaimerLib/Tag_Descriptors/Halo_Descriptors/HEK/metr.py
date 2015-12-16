from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return METR_Definition

class METR_Definition(Tag_Def):

    Ext = ".meter"

    Cls_ID = "metr"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"meter",
                     0:Combine( {1:{ DEFAULT:"metr" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:172, GUI_NAME:"Data",
                         0:{ TYPE:Struct, OFFSET:4, GUI_NAME:"Stencil Bitmap",
                              ATTRS:Tag_Reference_Structure
                             },
                         1:{ TYPE:Struct, OFFSET:20, GUI_NAME:"Source Bitmap",
                              ATTRS:Tag_Reference_Structure
                             },
                         2:{ TYPE:UInt16, OFFSET:36, GUI_NAME:"Stencil Sequence Index" },
                         3:{ TYPE:UInt16, OFFSET:38, GUI_NAME:"Source Sequence Index" },
                         4:{ TYPE:Enum16, OFFSET:60, GUI_NAME:"Interpolate Colors" ,
                              OPTIONS:{ 0:{GUI_NAME:"Linearly"},
                                        1:{GUI_NAME:"Faster near empty"},
                                        2:{GUI_NAME:"Faster near full"},
                                        3:{GUI_NAME:"Through random noise"}
                                        }
                              },
                         5:{ TYPE:Enum16, OFFSET:62, GUI_NAME:"Anchor Colors" ,
                              OPTIONS:{ 0:{GUI_NAME:"At both ends"},
                                        1:{GUI_NAME:"At empty"},
                                        2:{GUI_NAME:"At full"}
                                        }
                              },
                         6:Combine({OFFSET:72, GUI_NAME:"Empty Color"}, A_R_G_B_Float),
                         7:Combine({OFFSET:88, GUI_NAME:"Full Color"}, A_R_G_B_Float),
                         
                         8:{ TYPE:Float, OFFSET:124, GUI_NAME:"Unmask Distance" },
                         9:{ TYPE:Float, OFFSET:128, GUI_NAME:"Mask Distance" },
                     
                         10:{ TYPE:UInt8, OFFSET:144, GUI_NAME:"UNKNOWN_1 Width" },
                         11:{ TYPE:UInt8, OFFSET:146, GUI_NAME:"UNKNOWN_1 Heigth" },
                         12:{ TYPE:UInt8, OFFSET:148, GUI_NAME:"UNKNOWN_2 Width" },
                         13:{ TYPE:UInt8, OFFSET:150, GUI_NAME:"UNKNOWN_2 Height" },
                     
                         14:{ TYPE:Struct, OFFSET:152, GUI_NAME:"Pixel Data", EDITABLE:False ,
                             ATTRS:Raw_Data_Reference_Structure,
                             CHILD:{TYPE:Bytearray_Raw, NAME:"Data", SIZE:".Byte_Count"}
                             }
                         }
                     }
