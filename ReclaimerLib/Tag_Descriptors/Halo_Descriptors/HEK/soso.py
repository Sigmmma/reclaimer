from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from .Objs.soso import SOSO_Tag

def Construct():
    return SOSO_Definition

class SOSO_Definition(Tag_Def):

    Ext = ".shader_model"

    Cls_ID = "soso"
    
    Tag_Obj = SOSO_Tag

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"shader_model",
                     0:Combine( {1:{ DEFAULT:"soso" },
                                 5:{ DEFAULT:2 }
                                 }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:440, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader TYPE
                        1:Material_Type,
                        2:Numeric_Shader_ID,
                        
                        #Model Shader Properties
                        3:{ TYPE:Bool16, OFFSET:40, GUI_NAME:"Flags",
                            OPTIONS:{ 0:{GUI_NAME:"Detail After Reflection"},
                                      1:{GUI_NAME:"Two-Sided"},
                                      2:{GUI_NAME:"Not Alpha-Tested"},
                                      3:{GUI_NAME:"Alpha-Blended Decal"},
                                      4:{GUI_NAME:"True Atmospheric Fog"},
                                      5:{GUI_NAME:"Disable Two-Sided Culling"}
                                      }
                            },
                        4:{ TYPE:Float, OFFSET:56, GUI_NAME:"Translucency" },
                        
                        #Color-Change
                        5:{ TYPE:Enum16, OFFSET:76, GUI_NAME:"Color Change Source",
                            OPTIONS:Function_Names},
                            
                        #Self-Illumination
                        6:{TYPE:Struct, OFFSET:108, GUI_NAME:"Animation",
                           0:{ TYPE:Bool16, OFFSET:0, GUI_NAME:"Flags",
                               OPTIONS:{0:{GUI_NAME:"No Random Phase"}}
                               },
                           1:{ TYPE:Enum16, OFFSET:4, GUI_NAME:"Color Source",
                               OPTIONS:Function_Names
                               },
                           2:{ TYPE:Enum16, OFFSET:6, GUI_NAME:"Animation Function" ,
                               OPTIONS:Animation_Functions
                               },
                           3:{ TYPE:Float, OFFSET:8, GUI_NAME:"Animation Period"},#seconds
                           4:Combine({OFFSET:12, GUI_NAME:"Animation Color Lower Bound"}, R_G_B_Float),
                           5:Combine({OFFSET:24, GUI_NAME:"Animation Color Upper Bound"}, R_G_B_Float)
                           },
                            
                        #Diffuse, Multipurpose, and Detail Maps
                        7:{ TYPE:Struct, OFFSET:156, GUI_NAME:"Diffuse, Multipurpose, and Detail Maps",
                            0:{ TYPE:Float, OFFSET:0, GUI_NAME:"Map U-Scale" },
                            1:{ TYPE:Float, OFFSET:4, GUI_NAME:"Map V-Scale" },
                            2:{ TYPE:Struct, OFFSET:8, GUI_NAME:"Diffuse Map",
                                ATTRIBUTES:Tag_Reference_Structure
                                },
                            3:{ TYPE:Struct, OFFSET:32, GUI_NAME:"Multipurpose Map",
                                ATTRIBUTES:Tag_Reference_Structure
                                },
                             
                            4:{ TYPE:Enum16, OFFSET:56, GUI_NAME:"Detail Function" ,
                                OPTIONS:Detail_Map_Functions
                                },
                             
                            5:{ TYPE:Enum16, OFFSET:58, GUI_NAME:"Detail Mask" ,
                                OPTIONS:{ 0:{GUI_NAME:"None"},
                                          1:{GUI_NAME:"Red Inverse"},
                                          2:{GUI_NAME:"Red"},
                                          3:{GUI_NAME:"Green Inverse"},
                                          4:{GUI_NAME:"Green"},
                                          5:{GUI_NAME:"Blue Inverse"},
                                          6:{GUI_NAME:"Blue"},
                                          7:{GUI_NAME:"Alpha Inverse"},
                                          8:{GUI_NAME:"Alpha"}
                                          }
                                },
                              
                            6:{ TYPE:Float, OFFSET:60, GUI_NAME:"Detail Map Scale" },
                            7:{ TYPE:Struct, OFFSET:64, GUI_NAME:"Detail Map",
                                ATTRIBUTES:Tag_Reference_Structure
                                },
                            8:{ TYPE:Float, OFFSET:80, GUI_NAME:"Detail Map V-Scale" },
                            },

                        
                        #OS Shader Model Extension
                        8:{ TYPE:Struct, OFFSET:240, GUI_NAME:"OS Shader Model Ext",
                            ATTRIBUTES:Block_Reference_Structure,
                            CHILD:{TYPE:Array, NAME:"OS_Shader_Model_Ext_Array",
                                   MAX:1, SIZE:".Block_Count",
                                   SUB_STRUCT:{ TYPE:Struct, SIZE:192, GUI_NAME:"Shader Model Ext",
                                                #Specular Color
                                                0:{ TYPE:Struct, OFFSET:0, GUI_NAME:"Specular Color Map",
                                                    ATTRIBUTES:Tag_Reference_Structure
                                                    },
                                                1:{ TYPE:Float, OFFSET:16, GUI_NAME:"Specular Color Coefficient" },
                                                2:{ TYPE:Float, OFFSET:24, GUI_NAME:"Specular Color Exponent" },
                                                3:{ TYPE:Bool16, OFFSET:28, GUI_NAME:"Flags",
                                                    OPTIONS:{0:{GUI_NAME:"Alpha as Exponent Mask"}}
                                                    },

                                                #Base Normal Map
                                                4:{ TYPE:Struct, OFFSET:32, GUI_NAME:"Base Normal Map",
                                                    ATTRIBUTES:Tag_Reference_Structure
                                                    },
                                                5:{ TYPE:Float, OFFSET:48, GUI_NAME:"Base Normal Coefficient" },

                                                #Detail Normal Maps
                                                6:{ TYPE:Struct, OFFSET:64, GUI_NAME:"Detail Normal 1 Map",
                                                    ATTRIBUTES:Tag_Reference_Structure
                                                    },
                                                7:{ TYPE:Float, OFFSET:80, GUI_NAME:"Detail Normal 1 Coefficient" },
                                                8:{ TYPE:Float, OFFSET:84, GUI_NAME:"Detail Normal 1 Scale" },
                                                9:{ TYPE:Float, OFFSET:88, GUI_NAME:"Detail Normal 1 V-Scale" },
                                               
                                                10:{ TYPE:Struct, OFFSET:96, GUI_NAME:"Detail Normal 2 Map",
                                                     ATTRIBUTES:Tag_Reference_Structure
                                                     },
                                                11:{ TYPE:Float, OFFSET:112, GUI_NAME:"Detail Normal 2 Coefficient" },
                                                12:{ TYPE:Float, OFFSET:116, GUI_NAME:"Detail Normal 2 Scale" },
                                                13:{ TYPE:Float, OFFSET:120, GUI_NAME:"Detail Normal 2 V-Scale" },
                                               
                                                #Specular Tint Override
                                                14:{ TYPE:Float, OFFSET:128, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                                                15:Combine({OFFSET:132, GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                                               
                                                16:{ TYPE:Float, OFFSET:144, GUI_NAME:"Parallel Brightness"},#[0,1]
                                                17:Combine({OFFSET:148, GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                                               
                                                18:{ TYPE:Float, OFFSET:168, GUI_NAME:"Specular Lighting Exponent" },
                                                19:{ TYPE:Float, OFFSET:172, GUI_NAME:"Specular Lighting Coefficient" },
                                                }
                                   }
                            },

                            
                        #Texture Scrolling Animation
                        9:{ TYPE:Struct, OFFSET:252, GUI_NAME:"Texture Scrolling",
                            0:{TYPE:Struct, OFFSET:0, GUI_NAME:"U-Animation",
                               ATTRIBUTES:Anim_Src_Func_Per_Pha_Sca
                               },
                            1:{TYPE:Struct, OFFSET:16, GUI_NAME:"V-Animation",
                               ATTRIBUTES:Anim_Src_Func_Per_Pha_Sca
                               },
                            2:{TYPE:Struct, OFFSET:32, GUI_NAME:"Rotation-Animation",
                               ATTRIBUTES:Anim_Src_Func_Per_Pha_Sca
                               },
                            3:Combine({OFFSET:48, GUI_NAME:"Rot-Animation Center"}, X_Y_Float)
                            },
                            
                        #Reflection Properties
                        10:{ TYPE:Struct, OFFSET:316, GUI_NAME:"Reflection Properties",
                            0:{ TYPE:Float, OFFSET:0, GUI_NAME:"Falloff Distance"},#world units
                            1:{ TYPE:Float, OFFSET:4, GUI_NAME:"Cutoff Distance"},#world units
                         
                            2:{ TYPE:Float, OFFSET:8, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                            3:Combine({OFFSET:12, GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                            4:{ TYPE:Float, OFFSET:24, GUI_NAME:"Parallel Brightness"},#[0,1]
                            5:Combine({OFFSET:28, GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                             
                            6:{ TYPE:Struct, OFFSET:40, GUI_NAME:"Reflection Cube Map",
                                ATTRIBUTES:Tag_Reference_Structure
                                }
                            }
                        }
                     }
