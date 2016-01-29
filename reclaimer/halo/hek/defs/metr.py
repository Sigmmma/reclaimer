from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return MetrDef

class MetrDef(TagDef):

    ext = ".meter"

    tag_id = "metr"

    endian = ">"

    def linesize(*args, **kwargs):
        parent = kwargs.get('parent')
        
        if parent is None:
            raise KeyError

        if 'new_value' not in kwargs:
            width = parent.Width
            if width is not None:
                return 4*width
            return 0
        
        parent.Set_Neighbor('.Width', kwargs['new_value']//4)


    def has_next_line(*args, **kwargs):
        raw_data = kwargs.get('raw_data')
        
        if hasattr(raw_data, 'peek'):
            try:
                data = raw_data.peek(6)
                if len(data) >= 6:
                    return True
            except Exception:
                pass
        return False
    

    Meter_Line = { TYPE:Container, NAME:"Meter_Line",
                   0:{ TYPE:FlUInt16, NAME:"X_Pos" },
                   1:{ TYPE:FlUInt16, NAME:"Y_Pos" },
                   2:{ TYPE:FlUInt16, NAME:"Width" },
                   3:{ TYPE:BytesRaw, NAME:"Line_Data", SIZE:linesize }
                   }

    Meter_Image = { TYPE:WhileArray, NAME:"Data",
                    CASE:has_next_line, SUB_STRUCT:Meter_Line
                    }

    descriptor = {TYPE:Container, GUI_NAME:"meter",
                     0:com( {1:{ DEFAULT:"metr" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:172, GUI_NAME:"Data",
                         0:{ TYPE:TagIndexRef, OFFSET:4, GUI_NAME:"Stencil Bitmap",
                              INCLUDE:Tag_Index_Ref_Struct
                             },
                         1:{ TYPE:TagIndexRef, OFFSET:20, GUI_NAME:"Source Bitmap",
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
                         6:com({OFFSET:72, GUI_NAME:"Empty Color"}, A_R_G_B_Float),
                         7:com({OFFSET:88, GUI_NAME:"Full Color"}, A_R_G_B_Float),
                         
                         8:{ TYPE:Float, OFFSET:124, GUI_NAME:"Unmask Distance" },
                         9:{ TYPE:Float, OFFSET:128, GUI_NAME:"Mask Distance" },
                     
                         10:{ TYPE:FlUInt16, OFFSET:144, NAME:"Screen_X_Pos" },
                         11:{ TYPE:FlUInt16, OFFSET:146, NAME:"Screen_Y_Pos" },
                         12:{ TYPE:FlUInt16, OFFSET:148, NAME:"Meter_Width"  },
                         13:{ TYPE:FlUInt16, OFFSET:150, NAME:"Meter_Height" },
                     
                         14:{ TYPE:RawDataRef, OFFSET:152, GUI_NAME:"Meter Data", EDITABLE:False ,
                              INCLUDE:Raw_Data_Ref_Struct,
                              CHILD:{TYPE:BytearrayRaw, NAME:"Data", SIZE:".Count"}
                              #CHILD:Meter_Image
                              }
                         }
                     }

    descriptors = {"Meter_Image":Meter_Image}
