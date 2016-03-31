from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return SmetDef

class SmetDef(TagDef):

    ext = ".shader_transparent_meter"

    def_id = "smet"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"shader_meter",
                     0:com( {1:{ DEFAULT:"smet" }}, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:260, GUI_NAME:"Data",
                         #Radiosity Properties
                         0:Radiosity_Block,
                            
                         #Shader Type
                         1:Material_Type,
                         2:Numeric_Shader_ID,
                        
                         #Meter Shader Properties
                         3:{ TYPE:Bool16, OFFSET:40, GUI_NAME:"Meter Shader Flags" ,
                             0:{GUI_NAME:"Decal"},
                             1:{GUI_NAME:"Two-sided"},
                             2:{GUI_NAME:"Flash color is negative"},
                             3:{GUI_NAME:"Tint mode-2"},
                             4:{GUI_NAME:"Unfiltered"}
                             },
                         4:{ TYPE:TagIndexRef, OFFSET:76, GUI_NAME:"Meter Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                         
                         #Colors
                         5:com({OFFSET:124, GUI_NAME:"Gradient Min Color"}, R_G_B_Float),
                         6:com({OFFSET:136, GUI_NAME:"Gradient Max Color"}, R_G_B_Float),
                         7:com({OFFSET:148, GUI_NAME:"Background Color"}, R_G_B_Float),
                         8:com({OFFSET:160, GUI_NAME:"Flash Color"}, R_G_B_Float),
                         9:com({OFFSET:172, GUI_NAME:"Tint Color"}, R_G_B_Float),
                         10:{ TYPE:Float, OFFSET:184, GUI_NAME:"Meter Transparency" },
                         11:{ TYPE:Float, OFFSET:188, GUI_NAME:"Background Transparency" },

                         #External Function Sources
                         12:com({TYPE:Enum16, OFFSET:216, GUI_NAME:"Meter Brightness Source"},
                                Function_Outputs ),
                         13:com({TYPE:Enum16, OFFSET:218, GUI_NAME:"Flash Brightness Source"},
                                Function_Outputs ),
                         14:com({TYPE:Enum16, OFFSET:220, GUI_NAME:"Value Source"},
                                Function_Outputs ),
                         15:com({TYPE:Enum16, OFFSET:222, GUI_NAME:"Gradient Source"},
                                Function_Outputs ),
                         16:com({TYPE:Enum16, OFFSET:224, GUI_NAME:"Flash-Extension Source"},
                                Function_Outputs ),
                         }
                     }
