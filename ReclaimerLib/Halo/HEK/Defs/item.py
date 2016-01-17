from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return ITEM_Def

class ITEM_Def(Tag_Def):

    Ext = ".item"

    Cls_ID = "item"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"item",
                     0:Combine( {1:{ DEFAULT:"item" },
                                 5:{ DEFAULT:2 } },
                                Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:396, GUI_NAME:"Data",
                        0:{ TYPE:Pad, SIZE:2 },
                        1:{ TYPE:Bool16, GUI_NAME:"Flags",
                            0:{GUI_NAME:"Always maintains z up"},
                            1:{GUI_NAME:"Destroyed by explosions"},
                            2:{GUI_NAME:"Unaffected by gravity"},
                            },

                        2:{ TYPE:SInt16, GUI_NAME:"Message Index" },
                        3:{ TYPE:SInt16, GUI_NAME:"Sort Order" },
                        4:{ TYPE:Float,  GUI_NAME:"Scale" },
                        5:{ TYPE:SInt16, GUI_NAME:"Hud Message Value Scale" },

                        6:{ TYPE:Pad, SIZE:18 },

                        7:Com({TYPE:Enum16,  NAME:"A In" }, Device_Functions),
                        8:Com({TYPE:Enum16,  NAME:"B In" }, Device_Functions),
                        9:Com({TYPE:Enum16,  NAME:"C In" }, Device_Functions),
                        10:Com({TYPE:Enum16, NAME:"D In" }, Device_Functions),
                        
                        11:{ TYPE:Pad, SIZE:164 },
                        
                        12:{ TYPE:Tag_Index_Ref, GUI_NAME:"Material Effects",
                             INCLUDE:Tag_Index_Ref_Struct },
                        13:{ TYPE:Tag_Index_Ref, GUI_NAME:"Collision Sound",
                             INCLUDE:Tag_Index_Ref_Struct },
                        
                        14:{ TYPE:Pad, SIZE:120 },
                        
                        15:Com({ GUI_NAME:"Detonation Delay" }, From_To),
                        
                        16:{ TYPE:Tag_Index_Ref, GUI_NAME:"Detonating Effect",
                             INCLUDE:Tag_Index_Ref_Struct },
                        17:{ TYPE:Tag_Index_Ref, GUI_NAME:"Detonation Effect",
                             INCLUDE:Tag_Index_Ref_Struct }
                        }
                     }
