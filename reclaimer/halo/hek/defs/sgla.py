from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return SglaDef

class SglaDef(TagDef):

    ext = ".shader_glass"

    def_id = "sgla"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"shader_glass",
                     0:com( {1:{ DEFAULT:"sgla" }}, Tag_Header),
                     
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
                         4:com({OFFSET:84, GUI_NAME:"Background Tint Color"}, R_G_B_Float),
                         5:{ TYPE:Float, OFFSET:96, GUI_NAME:"Background Tint Map Scale" },
                         6:{ TYPE:TagIndexRef, OFFSET:100, GUI_NAME:"Background Tint Map",
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                         
                         #Reflection Properties
                         7:{ TYPE:Enum16, OFFSET:138, GUI_NAME:"Reflection Type" ,
                             0:{GUI_NAME:"Bumped Cubemap"},
                             1:{GUI_NAME:"Flat Cubemap"},
                             2:{GUI_NAME:"Dynamic Mirror"}
                             },
                         
                         8:{ TYPE:Float, OFFSET:140, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                         9:com({OFFSET:144, GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                         10:{ TYPE:Float, OFFSET:156, GUI_NAME:"Parallel Brightness"},#[0,1]
                         11:com({OFFSET:160,GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                         
                         12:{ TYPE:TagIndexRef, OFFSET:172, GUI_NAME:"Reflection Map",
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         
                         13:{ TYPE:Float, OFFSET:188, GUI_NAME:"Bump Map Scale" },
                         14:{ TYPE:TagIndexRef, OFFSET:192, GUI_NAME:"Bump Map" ,
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         
                         #Diffuse Properties
                         15:{ TYPE:Float, OFFSET:340, GUI_NAME:"Diffuse Map Scale" },
                         16:{ TYPE:TagIndexRef, OFFSET:344, GUI_NAME:"Diffuse Map",
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         17:{ TYPE:Float, OFFSET:360, GUI_NAME:"Diffuse Detail Map Scale" },
                         18:{ TYPE:TagIndexRef, OFFSET:364, GUI_NAME:"Diffuse Detail Map" ,
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         
                         #Specular Properties
                         19:{ TYPE:Float, OFFSET:412, GUI_NAME:"Specular Map Scale" },
                         20:{ TYPE:TagIndexRef, OFFSET:416, GUI_NAME:"Specular Map",
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         21:{ TYPE:Float, OFFSET:432, GUI_NAME:"Specular Detail Map Scale" },
                         22:{ TYPE:TagIndexRef, OFFSET:436, GUI_NAME:"Specular Detail Map" ,
                              INCLUDE:Tag_Index_Ref_Struct
                              },
                         }
                     }
