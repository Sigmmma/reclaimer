from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from .objs.soso import SosoTag

def get():
    return SosoDef

class SosoDef(TagDef):

    ext = ".shader_model"

    def_id = "soso"
    
    tag_cls = SosoTag

    endian = ">"

    OS_Shader_Model_Ext = { TYPE:Struct, SIZE:192, GUI_NAME:"Shader Model Ext",
                            #Specular Color
                            0:{ TYPE:TagIndexRef, OFFSET:0, GUI_NAME:"Specular Color Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                },
                            1:{ TYPE:Float, OFFSET:16, GUI_NAME:"Specular Color Coefficient" },
                            2:{ TYPE:Float, OFFSET:24, GUI_NAME:"Specular Color Exponent" },
                            3:{ TYPE:Bool16, OFFSET:28, GUI_NAME:"Flags",
                                0:{GUI_NAME:"Alpha as exponent mask"}
                                },

                            #Base Normal Map
                            4:{ TYPE:TagIndexRef, OFFSET:32, GUI_NAME:"Base Normal Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                },
                            5:{ TYPE:Float, OFFSET:48, GUI_NAME:"Base Normal Coefficient" },

                            #Detail Normal Maps
                            6:{ TYPE:TagIndexRef, OFFSET:64, GUI_NAME:"Detail Normal 1 Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                },
                            7:{ TYPE:Float, OFFSET:80, GUI_NAME:"Detail Normal 1 Coefficient" },
                            8:{ TYPE:Float, OFFSET:84, GUI_NAME:"Detail Normal 1 Scale" },
                            9:{ TYPE:Float, OFFSET:88, GUI_NAME:"Detail Normal 1 V-Scale" },
                           
                            10:{ TYPE:TagIndexRef, OFFSET:96, GUI_NAME:"Detail Normal 2 Map",
                                 INCLUDE:Tag_Index_Ref_Struct
                                 },
                            11:{ TYPE:Float, OFFSET:112, GUI_NAME:"Detail Normal 2 Coefficient" },
                            12:{ TYPE:Float, OFFSET:116, GUI_NAME:"Detail Normal 2 Scale" },
                            13:{ TYPE:Float, OFFSET:120, GUI_NAME:"Detail Normal 2 V-Scale" },
                           
                            #Specular Tint Override
                            14:{ TYPE:Float, OFFSET:128, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                            15:com({OFFSET:132, GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                           
                            16:{ TYPE:Float, OFFSET:144, GUI_NAME:"Parallel Brightness"},#[0,1]
                            17:com({OFFSET:148, GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                           
                            18:{ TYPE:Float, OFFSET:168, GUI_NAME:"Specular Lighting Exponent" },
                            19:{ TYPE:Float, OFFSET:172, GUI_NAME:"Specular Lighting Coefficient" },
                            }

    descriptor = {TYPE:Container, GUI_NAME:"shader_model",
                     0:com( {1:{ DEFAULT:"soso" },
                             5:{ DEFAULT:2 }
                                 }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:440, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader Type
                        1:Material_Type,
                        2:Numeric_Shader_ID,
                        
                        #Model Shader Properties
                        3:{ TYPE:Bool16, OFFSET:40, GUI_NAME:"Flags",
                            0:{GUI_NAME:"Detail after reflection"},
                            1:{GUI_NAME:"Two-sided"},
                            2:{GUI_NAME:"Not alpha-tested"},
                            3:{GUI_NAME:"Alpha-blended decal"},
                            4:{GUI_NAME:"True atmospheric fog"},
                            5:{GUI_NAME:"Disable two-sided culling"}
                            },
                        4:{ TYPE:Float, OFFSET:56, GUI_NAME:"Translucency" },
                        
                        #Color-Change
                        5:com({ TYPE:Enum16, OFFSET:76, GUI_NAME:"Color Change Source"},
                                Function_Names),
                            
                        #Self-Illumination
                        6:{TYPE:Struct, OFFSET:108, GUI_NAME:"Animation",
                           0:{ TYPE:Bool16, OFFSET:0, GUI_NAME:"Flags",
                               0:{GUI_NAME:"No random phase"} },
                           1:com({ TYPE:Enum16, OFFSET:4, GUI_NAME:"Color Source"},
                                 Function_Names),
                           2:com({ TYPE:Enum16, OFFSET:6, GUI_NAME:"Animation Function"},
                                 Animation_Functions),
                           3:{ TYPE:Float, OFFSET:8, GUI_NAME:"Animation Period"},#seconds
                           4:com({OFFSET:12, GUI_NAME:"Animation Color Lower Bound"}, R_G_B_Float),
                           5:com({OFFSET:24, GUI_NAME:"Animation Color Upper Bound"}, R_G_B_Float)
                           },
                            
                        #Diffuse, Multipurpose, and Detail Maps
                        7:{ TYPE:Struct, OFFSET:156, GUI_NAME:"Diffuse, Multipurpose, and Detail Maps",
                            0:{ TYPE:Float, OFFSET:0, GUI_NAME:"Map U-Scale" },
                            1:{ TYPE:Float, OFFSET:4, GUI_NAME:"Map V-Scale" },
                            2:{ TYPE:TagIndexRef, OFFSET:8, GUI_NAME:"Diffuse Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                },
                            3:{ TYPE:TagIndexRef, OFFSET:32, GUI_NAME:"Multipurpose Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                },
                             
                            4:com({ TYPE:Enum16, OFFSET:56, GUI_NAME:"Detail Function"},
                                    Detail_Map_Functions),
                             
                            5:{ TYPE:Enum16, OFFSET:58, GUI_NAME:"Detail Mask" ,
                                0:{GUI_NAME:"None"},
                                1:{GUI_NAME:"Red inverse"},
                                2:{GUI_NAME:"Red"},
                                3:{GUI_NAME:"Green inverse"},
                                4:{GUI_NAME:"Green"},
                                5:{GUI_NAME:"Blue inverse"},
                                6:{GUI_NAME:"Blue"},
                                7:{GUI_NAME:"Alpha inverse"},
                                8:{GUI_NAME:"Alpha"}
                                },
                              
                            6:{ TYPE:Float, OFFSET:60, GUI_NAME:"Detail Map Scale" },
                            7:{ TYPE:TagIndexRef, OFFSET:64, GUI_NAME:"Detail Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                },
                            8:{ TYPE:Float, OFFSET:80, GUI_NAME:"Detail Map V-Scale" },
                            },

                        
                        #OS Shader Model Extension
                        8:{ TYPE:Reflexive, OFFSET:240, GUI_NAME:"OS Shader Model Ext",
                            INCLUDE:Reflexive_Struct,
                            CHILD:{TYPE:Array, NAME:"OS_Shader_Model_Ext_Array",
                                   MAX:1, SIZE:".Count",
                                   SUB_STRUCT:OS_Shader_Model_Ext
                                   }
                            },

                            
                        #Texture Scrolling Animation
                        9:{ TYPE:Struct, OFFSET:252, GUI_NAME:"Texture Scrolling",
                            0:{TYPE:Struct, OFFSET:0, GUI_NAME:"U-Animation",
                               INCLUDE:Anim_Src_Func_Per_Pha_Sca },
                            1:{TYPE:Struct, OFFSET:16, GUI_NAME:"V-Animation",
                               INCLUDE:Anim_Src_Func_Per_Pha_Sca },
                            2:{TYPE:Struct, OFFSET:32, GUI_NAME:"Rotation-Animation",
                               INCLUDE:Anim_Src_Func_Per_Pha_Sca },
                            3:com({OFFSET:48, GUI_NAME:"Rot-Animation Center"}, X_Y_Float)
                            },
                            
                        #Reflection Properties
                        10:{ TYPE:Struct, OFFSET:316, GUI_NAME:"Reflection Properties",
                            0:{ TYPE:Float, OFFSET:0, GUI_NAME:"Falloff Distance"},#world units
                            1:{ TYPE:Float, OFFSET:4, GUI_NAME:"Cutoff Distance"},#world units
                         
                            2:{ TYPE:Float, OFFSET:8, GUI_NAME:"Perpendicular Brightness"},#[0,1]
                            3:com({OFFSET:12, GUI_NAME:"Perpendicular Tint Color"}, R_G_B_Float),
                            4:{ TYPE:Float, OFFSET:24, GUI_NAME:"Parallel Brightness"},#[0,1]
                            5:com({OFFSET:28, GUI_NAME:"Parallel Tint Color"}, R_G_B_Float),
                             
                            6:{ TYPE:TagIndexRef, OFFSET:40, GUI_NAME:"Reflection Cube Map",
                                INCLUDE:Tag_Index_Ref_Struct
                                }
                            }
                        }
                     }
