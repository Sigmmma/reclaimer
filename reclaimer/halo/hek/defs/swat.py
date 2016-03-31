from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return SwatDef

class SwatDef(TagDef):

    ext = ".shader_transparent_water"

    def_id = "swat"

    endian = ">"

    Ripples_Struct = { TYPE:Struct, SIZE:76, GUI_NAME:"Ripple",
                       0:{ TYPE:Float,  OFFSET:4, GUI_NAME:"Contribution Factor" },
                       1:{ TYPE:Float,  OFFSET:40, GUI_NAME:"Animation Angle" },
                       2:{ TYPE:Float,  OFFSET:44, GUI_NAME:"Animation Velocity" },
                       3:{ TYPE:Struct, OFFSET:48, GUI_NAME:"Map Offset",
                           0:{ TYPE:Float, GUI_NAME:"I" },
                           1:{ TYPE:Float, GUI_NAME:"J" }
                           },
                       4:{ TYPE:UInt16, OFFSET:56, GUI_NAME:"Map Repeats"},
                       5:{ TYPE:UInt16, OFFSET:58, GUI_NAME:"Map Index"},
                       }

    descriptor = {TYPE:Container, GUI_NAME:"shader_transparent_water",
                     0:com( {1:{ DEFAULT:"swat" },
                                 5:{ DEFAULT:2}
                                 }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:320, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader Type
                        1:Material_Type,
                        2:Numeric_Shader_ID,

                        #Water Shader Properties
                        3:{ TYPE:Bool16, OFFSET:40, GUI_NAME:"Flags",
                            0:{GUI_NAME:"Base map alpha modulates reflection"},
                            1:{GUI_NAME:"Base map color modulates background"},
                            2:{GUI_NAME:"Atmospheric fog"},
                            3:{GUI_NAME:"Draw before fog"},
                            },
                        4:{ TYPE:TagIndexRef, OFFSET:76, GUI_NAME:"Base Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                        5:{ TYPE:Float, OFFSET:108, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                        6:com({OFFSET:112,  GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                        7:{ TYPE:Float, OFFSET:124, GUI_NAME:"Parallel Brightness"},#[0,1]
                        8:com({OFFSET:128,  GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                        9:{ TYPE:TagIndexRef, OFFSET:156, GUI_NAME:"Reflection Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },

                        10:{ TYPE:Float, OFFSET:188, GUI_NAME:"Ripple Animation Angle"},
                        11:{ TYPE:Float, OFFSET:192, GUI_NAME:"Ripple Animation Velocity"},
                        12:{ TYPE:Float, OFFSET:196, GUI_NAME:"Ripple Scale"},
                        13:{ TYPE:TagIndexRef, OFFSET:200, GUI_NAME:"Ripple Maps",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                        14:{ TYPE:UInt16, OFFSET:216, GUI_NAME:"Ripple Mipmap Levels"},
                        15:{ TYPE:Float,  OFFSET:220, GUI_NAME:"Ripple Mipmap Fade Factor"},
                        16:{ TYPE:Float,  OFFSET:224, GUI_NAME:"Ripple Mipmap Detail Bias"},
                        
                        17:{ TYPE:Reflexive, OFFSET:292, GUI_NAME:"Ripples",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, NAME:"Ripples_Array",
                                    MAX:4, SIZE:".Count",
                                    SUB_STRUCT:Ripples_Struct
                                    }
                             }
                        }
                     }
