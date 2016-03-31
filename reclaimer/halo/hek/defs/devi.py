from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return DeviDef

class DeviDef(TagDef):

    ext = ".device"

    def_id = "devi"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"device",
                     0:com( {1:{ DEFAULT:"devi" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:276, GUI_NAME:"Data",
                        0:{ TYPE:Pad, SIZE:2 },
                        1:{ TYPE:Bool16, GUI_NAME:"Flags",
                            0:{GUI_NAME:"Position loops"},
                            1:{GUI_NAME:"Position not interpolated"},
                            },

                        2:{ TYPE:Float, GUI_NAME:"Power Transition Time" },
                        3:{ TYPE:Float, GUI_NAME:"Power Acceleration Time" },
                        4:{ TYPE:Float, GUI_NAME:"Position Transition Time" },
                        5:{ TYPE:Float, GUI_NAME:"Position Acceleration Time" },
                        6:{ TYPE:Float, GUI_NAME:"Depowered Position Transition Time" },
                        7:{ TYPE:Float, GUI_NAME:"Depowered Position Acceleration Time" },

                        8:com({TYPE:Enum16,  NAME:"A In" }, Device_Functions),
                        9:com({TYPE:Enum16,  NAME:"B In" }, Device_Functions),
                        10:com({TYPE:Enum16, NAME:"C In" }, Device_Functions),
                        11:com({TYPE:Enum16, NAME:"D In" }, Device_Functions),
                        
                        12:{ TYPE:TagIndexRef, GUI_NAME:"Open",
                             INCLUDE:Tag_Index_Ref_Struct },
                        13:{ TYPE:TagIndexRef, GUI_NAME:"Close",
                             INCLUDE:Tag_Index_Ref_Struct },
                        14:{ TYPE:TagIndexRef, GUI_NAME:"Opened",
                             INCLUDE:Tag_Index_Ref_Struct },
                        15:{ TYPE:TagIndexRef, GUI_NAME:"Closed",
                             INCLUDE:Tag_Index_Ref_Struct },
                        16:{ TYPE:TagIndexRef, GUI_NAME:"Depowered",
                             INCLUDE:Tag_Index_Ref_Struct },
                        17:{ TYPE:TagIndexRef, GUI_NAME:"Repowered",
                             INCLUDE:Tag_Index_Ref_Struct },
                        
                        18:{ TYPE:Float, GUI_NAME:"Delay Time" },
                        19:{ TYPE:TagIndexRef, GUI_NAME:"Delay Effect",
                             INCLUDE:Tag_Index_Ref_Struct, OFFSET:144 },
                        20:{ TYPE:Float, GUI_NAME:"Automatic Activation Radius" },
                        }
                     }
