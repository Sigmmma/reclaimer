from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return DEVI_Def

class DEVI_Def(Tag_Def):

    Ext = ".device"

    Cls_ID = "devi"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"device",
                     0:Combine( {1:{ DEFAULT:"devi" } }, Tag_Header),
                     
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

                        8:Com({TYPE:Enum16,  NAME:"A In" }, Device_Functions),
                        9:Com({TYPE:Enum16,  NAME:"B In" }, Device_Functions),
                        10:Com({TYPE:Enum16, NAME:"C In" }, Device_Functions),
                        11:Com({TYPE:Enum16, NAME:"D In" }, Device_Functions),
                        
                        12:{ TYPE:Tag_Index_Ref, GUI_NAME:"Open",
                             INCLUDE:Tag_Index_Ref_Struct },
                        13:{ TYPE:Tag_Index_Ref, GUI_NAME:"Close",
                             INCLUDE:Tag_Index_Ref_Struct },
                        14:{ TYPE:Tag_Index_Ref, GUI_NAME:"Opened",
                             INCLUDE:Tag_Index_Ref_Struct },
                        15:{ TYPE:Tag_Index_Ref, GUI_NAME:"Closed",
                             INCLUDE:Tag_Index_Ref_Struct },
                        16:{ TYPE:Tag_Index_Ref, GUI_NAME:"Depowered",
                             INCLUDE:Tag_Index_Ref_Struct },
                        17:{ TYPE:Tag_Index_Ref, GUI_NAME:"Repowered",
                             INCLUDE:Tag_Index_Ref_Struct },
                        
                        18:{ TYPE:Float, GUI_NAME:"Delay Time" },
                        19:{ TYPE:Tag_Index_Ref, GUI_NAME:"Delay Effect",
                             INCLUDE:Tag_Index_Ref_Struct, OFFSET:144 },
                        20:{ TYPE:Float, GUI_NAME:"Automatic Activation Radius" },
                        }
                     }
