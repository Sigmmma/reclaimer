from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return SplaDef

class SplaDef(TagDef):

    ext = ".shader_transparent_plasma"

    def_id = "spla"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"shader_transparent_plasma",
                     0:com( {1:{ DEFAULT:"spla" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:332, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader Type
                        1:Material_Type,
                        2:Numeric_Shader_ID,
                        
                        #Intensity
                        3:com({ TYPE:Enum16, OFFSET:44, GUI_NAME:"Intensity Source"},
                                Function_Outputs),
                        4:{ TYPE:Float, OFFSET:48, GUI_NAME:"Intensity Exponent"},
                        
                        #Offset
                        5:com({ TYPE:Enum16, OFFSET:52, GUI_NAME:"Offset Source"},
                                Function_Outputs),
                        6:{ TYPE:Float, OFFSET:56, GUI_NAME:"Offset Amount"},
                        7:{ TYPE:Float, OFFSET:60, GUI_NAME:"Offset Exponent"},
                            
                        #Color
                        8:{ TYPE:Float, OFFSET:96,   GUI_NAME:"Perpendicular Brightness"},#[0,1]
                        9:com({OFFSET:100,  GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                        10:{ TYPE:Float, OFFSET:112, GUI_NAME:"Parallel Brightness"},#[0,1]
                        11:com({OFFSET:116, GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                        12:com({TYPE:Enum16, OFFSET:128, GUI_NAME:"Tint Color Source"}, Function_Names),

                        #Primary Noise Map
                        13:{ TYPE:Float, OFFSET:192, GUI_NAME:"Primary Animation Period"},
                        14:com({OFFSET:196, GUI_NAME:"Primary Animation Direction"}, I_J_K_Float),
                        15:{ TYPE:Float, OFFSET:208, GUI_NAME:"Primary Noise Map Scale"},
                        16:{ TYPE:TagIndexRef, OFFSET:212, GUI_NAME:"Primary Noise Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                        
                        #Secondary Noise Map
                        17:{ TYPE:Float, OFFSET:264, GUI_NAME:"Secondary Animation Period"},
                        18:com({OFFSET:268, GUI_NAME:"Secondary Animation Direction"}, I_J_K_Float),
                        19:{ TYPE:Float, OFFSET:280, GUI_NAME:"Secondary Noise Map Scale"},
                        20:{ TYPE:TagIndexRef, OFFSET:284, GUI_NAME:"Secondary Noise Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                        }
                     }
