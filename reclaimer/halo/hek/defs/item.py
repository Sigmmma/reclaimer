from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return ItemDef

class ItemDef(TagDef):

    ext = ".item"

    def_id = "item"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"item",
                     0:com( {1:{ DEFAULT:"item" },
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

                        7:com({TYPE:Enum16,  NAME:"A In" }, Device_Functions),
                        8:com({TYPE:Enum16,  NAME:"B In" }, Device_Functions),
                        9:com({TYPE:Enum16,  NAME:"C In" }, Device_Functions),
                        10:com({TYPE:Enum16, NAME:"D In" }, Device_Functions),
                        
                        11:{ TYPE:Pad, SIZE:164 },
                        
                        12:{ TYPE:TagIndexRef, GUI_NAME:"Material Effects",
                             INCLUDE:Tag_Index_Ref_Struct },
                        13:{ TYPE:TagIndexRef, GUI_NAME:"Collision Sound",
                             INCLUDE:Tag_Index_Ref_Struct },
                        
                        14:{ TYPE:Pad, SIZE:120 },
                        
                        15:com({ GUI_NAME:"Detonation Delay" }, From_To),
                        
                        16:{ TYPE:TagIndexRef, GUI_NAME:"Detonating Effect",
                             INCLUDE:Tag_Index_Ref_Struct },
                        17:{ TYPE:TagIndexRef, GUI_NAME:"Detonation Effect",
                             INCLUDE:Tag_Index_Ref_Struct }
                        }
                     }
