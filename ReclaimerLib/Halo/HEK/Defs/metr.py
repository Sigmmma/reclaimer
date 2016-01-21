from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return METR_Def

class METR_Def(Tag_Def):

    Ext = ".meter"

    Cls_ID = "metr"

    Endian = ">"

    def Line_Size(*args, **kwargs):
        Parent = kwargs.get('Parent')
        
        if Parent is None:
            raise KeyError

        if 'New_Value' not in kwargs:
            Width = Parent.Width
            if Width is not None:
                return 4*Parent.Width
            return 0
        
        Parent.Set_Neighbor('.Width', kwargs['New_Value']//4)


    def Has_Next_Line(*args, **kwargs):
        Raw_Data = kwargs.get('Raw_Data')
        
        if hasattr(Raw_Data, 'peek'):
            try:
                Data = Raw_Data.peek(6)
                if len(Data) >= 6:
                    return True
            except Exception:
                pass
        return False
    

    Meter_Line = { TYPE:Container, NAME:"Meter_Line",
                   0:{ TYPE:FL_UInt16,    NAME:"X_Pos" },
                   1:{ TYPE:FL_UInt16,    NAME:"Y_Pos" },
                   2:{ TYPE:FL_UInt16,    NAME:"Width" },
                   3:{ TYPE:Bytes_Raw, NAME:"Line_Data", SIZE:Line_Size }
                   }

    Meter_Image = { TYPE:While_Array, NAME:"Data",
                    CASE:Has_Next_Line, SUB_STRUCT:Meter_Line
                    }

    Tag_Structure = {TYPE:Container, GUI_NAME:"meter",
                     0:Combine( {1:{ DEFAULT:"metr" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:172, GUI_NAME:"Data",
                         0:{ TYPE:Tag_Index_Ref, OFFSET:4, GUI_NAME:"Stencil Bitmap",
                              INCLUDE:Tag_Index_Ref_Struct
                             },
                         1:{ TYPE:Tag_Index_Ref, OFFSET:20, GUI_NAME:"Source Bitmap",
                              INCLUDE:Tag_Index_Ref_Struct
                             },
                         2:{ TYPE:SInt16, OFFSET:36, GUI_NAME:"Stencil Sequence Index" },
                         3:{ TYPE:SInt16, OFFSET:38, GUI_NAME:"Source Sequence Index" },
                         4:{ TYPE:Enum16, OFFSET:60, GUI_NAME:"Interpolate Colors" ,
                              0:{GUI_NAME:"Linearly"},
                              1:{GUI_NAME:"Faster near empty"},
                              2:{GUI_NAME:"Faster near full"},
                              3:{GUI_NAME:"Through random noise"}
                              },
                         5:{ TYPE:Enum16, OFFSET:62, GUI_NAME:"Anchor Colors" ,
                              0:{GUI_NAME:"At both ends"},
                              1:{GUI_NAME:"At empty"},
                              2:{GUI_NAME:"At full"}
                              },
                         6:Combine({OFFSET:72, GUI_NAME:"Empty Color"}, A_R_G_B_Float),
                         7:Combine({OFFSET:88, GUI_NAME:"Full Color"}, A_R_G_B_Float),
                         
                         8:{ TYPE:Float, OFFSET:124, GUI_NAME:"Unmask Distance" },
                         9:{ TYPE:Float, OFFSET:128, GUI_NAME:"Mask Distance" },
                     
                         10:{ TYPE:FL_UInt16, OFFSET:144, NAME:"Screen_X_Pos" },
                         11:{ TYPE:FL_UInt16, OFFSET:146, NAME:"Screen_Y_Pos" },
                         12:{ TYPE:FL_UInt16, OFFSET:148, NAME:"Meter_Width"  },
                         13:{ TYPE:FL_UInt16, OFFSET:150, NAME:"Meter_Height" },
                     
                         14:{ TYPE:Raw_Data_Ref, OFFSET:152, GUI_NAME:"Meter Data", EDITABLE:False ,
                              INCLUDE:Raw_Data_Ref_Struct,
                              CHILD:{TYPE:Bytearray_Raw, NAME:"Data", SIZE:".Count"}
                              #CHILD:Meter_Image
                              }
                         }
                     }

    Structures = {"Meter_Image":Meter_Image}
