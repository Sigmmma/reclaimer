from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return SGLA_Def

class SGLA_Def(Tag_Def):

    Ext = ".shader_glass"

    Cls_ID = "sgla"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"shader_glass",
                     0:Combine( {1:{ DEFAULT:"sgla" }}, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:480, GUI_NAME:"Data",
                         #Radiosity Properties
                         0:Radiosity_Block,
                            
                         #Shader Type
                         1:Material_Type,
                         2:Numeric_Shader_ID,
                        
                         #Environment Shader Properties
                         3:{ TYPE:Bool16, OFFSET:40, GUI_NAME:"Glass Shader Flags" ,
                             0:{GUI_NAME:"Alpha tested"},
                             1:{GUI_NAME:"Decal"},
                             2:{GUI_NAME:"Two-sided"},
                             3:{GUI_NAME:"Bump map is specular mask"}
                             },

                         #Background Tint Properties
                         4:Combine({OFFSET:84, GUI_NAME:"Background Tint Color"}, R_G_B_Float),
                         5:{ TYPE:Float, OFFSET:96, GUI_NAME:"Background Tint Map Scale" },
                         6:{ TYPE:Tag_Index_Ref, OFFSET:100, GUI_NAME:"Background Tint Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                         
                         #Reflection Properties
                         7:{ TYPE:Enum16, OFFSET:138, GUI_NAME:"Reflection Type" ,
                             0:{GUI_NAME:"Bumped Cubemap"},
                             1:{GUI_NAME:"Flat Cubemap"},
                             2:{GUI_NAME:"Dynamic Mirror"}
                             },
                         
                         8:{ TYPE:Float, OFFSET:140, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                         9:Combine({OFFSET:144,      GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                         10:{ TYPE:Float, OFFSET:156, GUI_NAME:"Parallel Brightness"},#[0,1]
                         11:Combine({OFFSET:160,      GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                         
                         12:{ TYPE:Tag_Index_Ref, OFFSET:172, GUI_NAME:"Reflection Map",
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         
                         13:{ TYPE:Float, OFFSET:188, GUI_NAME:"Bump Map Scale" },
                         14:{ TYPE:Tag_Index_Ref, OFFSET:192, GUI_NAME:"Bump Map" ,
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         
                         #Diffuse Properties
                         15:{ TYPE:Float, OFFSET:340, GUI_NAME:"Diffuse Map Scale" },
                         16:{ TYPE:Tag_Index_Ref, OFFSET:344, GUI_NAME:"Diffuse Map",
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         17:{ TYPE:Float, OFFSET:360, GUI_NAME:"Diffuse Detail Map Scale" },
                         18:{ TYPE:Tag_Index_Ref, OFFSET:364, GUI_NAME:"Diffuse Detail Map" ,
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         
                         #Specular Properties
                         19:{ TYPE:Float, OFFSET:412, GUI_NAME:"Specular Map Scale" },
                         20:{ TYPE:Tag_Index_Ref, OFFSET:416, GUI_NAME:"Specular Map",
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         21:{ TYPE:Float, OFFSET:432, GUI_NAME:"Specular Detail Map Scale" },
                         22:{ TYPE:Tag_Index_Ref, OFFSET:436, GUI_NAME:"Specular Detail Map" ,
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         }
                     }
