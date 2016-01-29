from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return Fog_Def

class Fog_Def(TagDef):

    ext = ".fog"

    tag_id = "fog "

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"fog",
                     0:com( {1:{ DEFAULT:"fog " } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:396, GUI_NAME:"Data",
                        #Fog Flags
                        0:{ TYPE:Bool32, OFFSET:0, GUI_NAME:"Fog Flags",
                            0:{GUI_NAME:"Is water"},
                            1:{GUI_NAME:"Atmospheric dominant"},
                            2:{GUI_NAME:"Fog screen only"},
                            },

                        #Density
                        1:{ TYPE:Float, OFFSET:88,  GUI_NAME:"Maximum Density" },
                        2:{ TYPE:Float, OFFSET:96,  GUI_NAME:"Opaque Distance" },
                        3:{ TYPE:Float, OFFSET:104, GUI_NAME:"Opaque Depth" },
                        4:{ TYPE:Float, OFFSET:116, GUI_NAME:"Distance to Water Plane" },

                        #Color
                        5:com({NAME:"Fog Color", OFFSET:120 }, R_G_B_Float),

                        #Screen Layers
                        6:{ TYPE:Bool16, OFFSET:132, GUI_NAME:"Flags",
                            0:{GUI_NAME:"No environment multipass"},
                            1:{GUI_NAME:"No model multipass"},
                            2:{GUI_NAME:"No texture-based falloff"},
                            },
                        7:{ TYPE:UInt16, OFFSET:134, GUI_NAME:"Layer Count" },
                        
                        8:com({NAME:"Distance Gradient", OFFSET:136}, From_To),
                        9:com({NAME:"Density Gradient", OFFSET:144}, From_To),
                        
                        10:{ TYPE:Float, OFFSET:152, GUI_NAME:"Start Distance from Fog Plane" },

                        11:com({ GUI_NAME:"Color", OFFSET:161 }, R_G_B_Byte),
                        12:{ TYPE:Float, OFFSET:164, GUI_NAME:"Rotation Multiplier" },
                        13:{ TYPE:Float, OFFSET:168, GUI_NAME:"Strafing Multiplier" },
                        14:{ TYPE:Float, OFFSET:172, GUI_NAME:"Zoom Multiplier" },
                        
                        15:{ TYPE:Float, OFFSET:184, GUI_NAME:"Map Scale" },
                        16:{ TYPE:TagIndexRef, OFFSET:188, GUI_NAME:"Fog Map",
                             SIZE:16, INCLUDE:Tag_Index_Ref_Struct
                             },

                        #Screen Layer Animation
                        17:{ TYPE:Float, OFFSET:204, GUI_NAME:"Animation Period" },
                        18:com({NAME:"Wind Velocity", OFFSET:212}, From_To),
                        19:com({NAME:"Wind Period", OFFSET:220}, From_To),
                        20:{ TYPE:Float, OFFSET:228, GUI_NAME:"Wind Acceleration Weight" },
                        21:{ TYPE:Float, OFFSET:232, GUI_NAME:"Wind Perpendicular Weight" },

                        #Sound
                        22:{ TYPE:TagIndexRef, OFFSET:244, GUI_NAME:"Background Sound",
                             SIZE:16, INCLUDE:Tag_Index_Ref_Struct
                             },
                        23:{ TYPE:TagIndexRef, OFFSET:260, GUI_NAME:"Sound Environment",
                             SIZE:16, INCLUDE:Tag_Index_Ref_Struct
                             },
                        }
                     }
