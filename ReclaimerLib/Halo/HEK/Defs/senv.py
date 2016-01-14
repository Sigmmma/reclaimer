from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from .Objs.senv import SENV_Tag

def Construct():
    return SENV_Definition

class SENV_Definition(Tag_Def):

    Ext = ".shader_environment"

    Cls_ID = "senv"

    Tag_Cls = SENV_Tag

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"shader_environment",
                     0:Combine( {1:{ DEFAULT:"senv" },
                                 5:{ DEFAULT:2 }
                                 }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:836, GUI_NAME:"Data",
                         #Radiosity Properties
                         0:Radiosity_Block,
                            
                         #Shader Type
                         1:Material_Type,
                         2:Numeric_Shader_ID,
                        
                         #Environment Shader Properties
                         3:{ TYPE:Bool16, OFFSET:40, GUI_NAME:"Environment Shader Flags" ,
                             0:{GUI_NAME:"Alpha Tested"},
                             1:{GUI_NAME:"Bump-map is Specular Mask"},
                             2:{GUI_NAME:"True Atmospheric Fog"}
                             },
                         4:{ TYPE:Enum16, OFFSET:42, GUI_NAME:"Environment Shader Type" ,
                              0:{GUI_NAME:"Normal"},
                              1:{GUI_NAME:"Blended"},
                              2:{GUI_NAME:"Blended Base Specular"}
                              },
                         
                         #Lens Flare
                         5:{ TYPE:Float, OFFSET:44, GUI_NAME:"Lens Flare Spacing"},#world units
                         6:{ TYPE:Struct, OFFSET:48, GUI_NAME:"Lens Flare" ,
                             INCLUDE:Tag_Reference_Structure
                         },
                         
                         #Diffuse Properties
                         7:{ TYPE:Bool16, OFFSET:108, GUI_NAME:"Diffuse Flags" ,
                             0:{GUI_NAME:"Rescale Detail Maps"},
                             1:{GUI_NAME:"Rescale Bump Maps"}
                             },
                         8:{ TYPE:Struct, OFFSET:136, GUI_NAME:"Base Map",
                             INCLUDE:Tag_Reference_Structure
                         },

                         9:Com({ TYPE:Enum16, OFFSET:176, GUI_NAME:"Detail Map Function"},
                               Detail_Map_Functions),
                         10:{ TYPE:Float, OFFSET:180, GUI_NAME:"Primary Detail Map Scale" },
                         11:{ TYPE:Struct, OFFSET:184, GUI_NAME:"Primary Detail Map" ,
                              INCLUDE:Tag_Reference_Structure
                         },
                         12:{ TYPE:Float, OFFSET:200, GUI_NAME:"Secondary Detail Map Scale" },
                         13:{ TYPE:Struct, OFFSET:204, GUI_NAME:"Secondary Detail Map" ,
                              INCLUDE:Tag_Reference_Structure
                         },

                         14:Com({ TYPE:Enum16, OFFSET:244, GUI_NAME:"Micro Detail Map Function"},
                                Detail_Map_Functions),
                         15:{ TYPE:Float, OFFSET:248, GUI_NAME:"Micro Detail Map Scale" },
                         16:{ TYPE:Struct, OFFSET:252, GUI_NAME:"Micro Detail Map" ,
                              INCLUDE:Tag_Reference_Structure
                         },
                         
                         17:Combine({OFFSET:268, GUI_NAME:"Material Color"}, R_G_B_Float),
                         
                         #Bump Properties
                         18:{ TYPE:Float, OFFSET:292, GUI_NAME:"Bump Map Scale" },
                         19:{ TYPE:Struct, OFFSET:296, GUI_NAME:"Bump Map" ,
                              INCLUDE:Tag_Reference_Structure
                         },
                         20:{ TYPE:Float, ENDIAN:"<", OFFSET:312, NAME:"UNKNOWN_1", GUI_NAME:"Unknown X" },
                         21:{ TYPE:Float, ENDIAN:"<", OFFSET:316, NAME:"UNKNOWN_2", GUI_NAME:"Unknown Y" },
                         
                         #Texture Animation
                         22:{TYPE:Struct, OFFSET:336, GUI_NAME:"U-Animation",
                             INCLUDE:Anim_Func_Per_Pha,
                             2:{ TYPE:Float, OFFSET:8, GUI_NAME:"Scale"}#base map repeats
                            },
                         23:{TYPE:Struct, OFFSET:336, GUI_NAME:"V-Animation",
                             INCLUDE:Anim_Func_Per_Pha,
                             2:{ TYPE:Float, OFFSET:8, GUI_NAME:"Scale"}#base map repeats
                            },
                         
                         #Self Illumination
                         24:Combine({OFFSET:412, GUI_NAME:"Primary On-Color"}, R_G_B_Float),
                         25:Combine({OFFSET:424, GUI_NAME:"Primary Off-Color"}, R_G_B_Float),
                         26:{TYPE:Struct, OFFSET:436, GUI_NAME:"Primary Animation",
                             INCLUDE:Anim_Func_Per_Pha
                             },
                         
                         27:Combine({OFFSET:472, GUI_NAME:"Secondary On-Color"}, R_G_B_Float),
                         28:Combine({OFFSET:484, GUI_NAME:"Secondary Off-Color"}, R_G_B_Float),
                         29:{TYPE:Struct, OFFSET:496, GUI_NAME:"Secondary Animation",
                             INCLUDE:Anim_Func_Per_Pha
                             },

                         30:Combine({OFFSET:532, GUI_NAME:"Plasma On-Color"}, R_G_B_Float),
                         31:Combine({OFFSET:544, GUI_NAME:"Plasma Off-Color"}, R_G_B_Float),
                         32:{TYPE:Struct, OFFSET:556, GUI_NAME:"Plasma Animation",
                             INCLUDE:Anim_Func_Per_Pha
                             },
                         
                         33:{ TYPE:Float, OFFSET:592, GUI_NAME:"Illumination Map Scale" },
                         34:{ TYPE:Struct, OFFSET:596, GUI_NAME:"Illumination Map" ,
                              INCLUDE:Tag_Reference_Structure
                         },

                         #Specular Properties
                         35:{ TYPE:Bool16, OFFSET:636, GUI_NAME:"Specular Flags" ,
                              0:{GUI_NAME:"Overbright"},
                              1:{GUI_NAME:"Extra-Shiny"},
                              2:{GUI_NAME:"Lightmap is Specular"}
                              },
                         36:{ TYPE:Float, OFFSET:656, GUI_NAME:"Brightness"},#[0,1]
                         
                         37:Combine({OFFSET:680, GUI_NAME:"Perpendicular Color"}, R_G_B_Float),
                         38:Combine({OFFSET:692, GUI_NAME:"Parallel Color"}, R_G_B_Float),
                         
                         #Reflection Properties
                         39:{ TYPE:Bool16, OFFSET:720, GUI_NAME:"Reflection Flags" ,
                              0:{GUI_NAME:"Dynamic Mirror"} },
                         40:{ TYPE:Enum16, OFFSET:722, GUI_NAME:"Reflection Type" ,
                              0:{GUI_NAME:"Bumped Cubemap"},
                              1:{GUI_NAME:"Flat Cubemap"},
                              2:{GUI_NAME:"Bumped Radiosity"}
                              },
                         
                         41:{ TYPE:Float, OFFSET:724, GUI_NAME:"Lightmap Brightness Scale"},#[0,1]
                         42:{ TYPE:Float, OFFSET:756, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                         43:{ TYPE:Float, OFFSET:760, GUI_NAME:"Parallel Brightness"},#[0,1]
                         
                         44:{ TYPE:Struct, OFFSET:804, GUI_NAME:"Reflection Cube Map",
                              INCLUDE:Tag_Reference_Structure
                              }
                          }
                     }
