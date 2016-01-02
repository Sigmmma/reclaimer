from supyr_struct.Defs.Common_Structures import *
from ..Field_Types import *

Com = Combine

#Enumerators for different types of tag references
All_Tag_Enums = {0:{VALUE:'actr', NAME:"actor"},
                 1:{VALUE:'actv', NAME:"actor_varient"},
                 2:{VALUE:'ant!', NAME:"antenna"},
                 3:{VALUE:'bipd', NAME:"biped"},
                 4:{VALUE:'bitm', NAME:"bitmap"},
                 5:{VALUE:'trak', NAME:"camera_track"},
                 6:{VALUE:'colo', NAME:"color_table"},
                 7:{VALUE:'cdmg', NAME:"continuous_damage_effect"},
                 8:{VALUE:'cont', NAME:"contrail"},
                 9:{VALUE:'deca', NAME:"decal"},
                 10:{VALUE:'udlg', NAME:"dialogue"},
                 11:{VALUE:'dobc', NAME:"detail_object_collection"},
                 12:{VALUE:'devi', NAME:"device"},
                 13:{VALUE:'ctrl', NAME:"device_control"},
                 14:{VALUE:'lifi', NAME:"device_light_fixture"},
                 15:{VALUE:'mach', NAME:"device_machine"},
                 16:{VALUE:'jpt!', NAME:"damage_effect"},
                 17:{VALUE:'effe', NAME:"effect"},
                 18:{VALUE:'eqip', NAME:"equipment"},
                 19:{VALUE:'flag', NAME:"flag"},
                 20:{VALUE:'fog ', NAME:"fog"},
                 21:{VALUE:'font', NAME:"font"},
                 22:{VALUE:'garb', NAME:"garbage"},
                 23:{VALUE:'mod2', NAME:"gbxmodel"},
                 24:{VALUE:'matg', NAME:"globals"},
                 25:{VALUE:'glw!', NAME:"glow"},
                 26:{VALUE:'grhi', NAME:"grenade_hud_interface"},
                 27:{VALUE:'hudg', NAME:"hud_globals"},
                 28:{VALUE:'hmt ', NAME:"hud_message_text"},
                 29:{VALUE:'hud#', NAME:"hud_number"},
                 30:{VALUE:'devc', NAME:"input_device_defaults"},
                 31:{VALUE:'item', NAME:"item"},
                 32:{VALUE:'itmc', NAME:"item_collection"},
                 33:{VALUE:'lens', NAME:"lens_flare"},
                 34:{VALUE:'ligh', NAME:"light"},
                 35:{VALUE:'mgs2', NAME:"light_volume"},
                 36:{VALUE:'elec', NAME:"lightning"},
                 37:{VALUE:'foot', NAME:"material_effects"},
                 38:{VALUE:'metr', NAME:"meter"},
                 39:{VALUE:'mode', NAME:"model"},
                 40:{VALUE:'antr', NAME:"model_animations"},
                 41:{VALUE:'coll', NAME:"model_collision_geometry"},
                 42:{VALUE:'mply', NAME:"multiplayer_scenario_description"},
                 43:{VALUE:'obje', NAME:"object"},
                 44:{VALUE:'part', NAME:"particle"},
                 45:{VALUE:'pctl', NAME:"particle_system"},
                 46:{VALUE:'phys', NAME:"physics"},
                 47:{VALUE:'plac', NAME:"placeholder"},
                 48:{VALUE:'pphy', NAME:"point_physics"},
                 49:{VALUE:'ngpr', NAME:"preferences_network_game"},
                 50:{VALUE:'proj', NAME:"projectile"},
                 51:{VALUE:'scnr', NAME:"scenario"},
                 52:{VALUE:'sbsp', NAME:"scenario_structure_bsp"},
                 53:{VALUE:'scen', NAME:"scenery"},
                 54:{VALUE:'snd!', NAME:"sound"},
                 55:{VALUE:'snde', NAME:"sound_environment"},
                 56:{VALUE:'lsnd', NAME:"sound_looping"},
                 57:{VALUE:'ssce', NAME:"sound_scenery"},
                 58:{VALUE:'boom', NAME:"spheroid"},
                 59:{VALUE:'shdr', NAME:"shader"},
                 60:{VALUE:'schi', NAME:"shader_transparent_chicago"},
                 61:{VALUE:'scex', NAME:"shader_transparent_chicago_extended"},
                 62:{VALUE:'sotr', NAME:"shader_transparent_generic"},
                 63:{VALUE:'senv', NAME:"shader_environment"},
                 64:{VALUE:'sgla', NAME:"shader_transparent_glass"},
                 65:{VALUE:'smet', NAME:"shader_transparent_meter"},
                 66:{VALUE:'soso', NAME:"shader_model"},
                 67:{VALUE:'spla', NAME:"shader_transparent_plasma"},
                 68:{VALUE:'swat', NAME:"shader_transparent_water"},
                 69:{VALUE:'sky ', NAME:"sky"},
                 70:{VALUE:'str#', NAME:"string_list"},
                 71:{VALUE:'tagc', NAME:"tag_collection"},
                 72:{VALUE:'Soul', NAME:"ui_widget_collection"},
                 73:{VALUE:'DeLa', NAME:"ui_widget_definition"},
                 74:{VALUE:'ustr', NAME:"unicode_string_list"},
                 75:{VALUE:'unit', NAME:"unit"},
                 76:{VALUE:'unhi', NAME:"unit_hud_interface"},
                 77:{VALUE:'vehi', NAME:"vehicle"},
                 78:{VALUE:'vcky', NAME:"virtual_keyboard"},
                 79:{VALUE:'weap', NAME:"weapon"},
                 80:{VALUE:'wphi', NAME:"weapon_hud_interface"},
                 81:{VALUE:'rain', NAME:"weather_particle_system"},
                 82:{VALUE:'wind', NAME:"wind"}
                 }

Tag_Header = { TYPE:Struct, SIZE:64, NAME:"Blam_Header", EDITABLE:False,
               0:{ PAD:36 },
               1:Com({TYPE:Str_Latin1_Enum, GUI_NAME:"Type FourCC", SIZE:4,
                      DEFAULT:b"\x00\x00\x00\x00"}, All_Tag_Enums),
               2:{ TYPE:UInt32, GUI_NAME:"Base Address", DEFAULT:0 },
               3:{ TYPE:UInt32, GUI_NAME:"Header Size", DEFAULT:64 },
               4:{ PAD:8 },
               5:{ TYPE:UInt16, NAME:"Version", DEFAULT:1 },
               6:{ TYPE:UInt16, NAME:"Unknown", DEFAULT:255 },
               7:{ TYPE:Str_Latin1_Enum, GUI_NAME:"Engine ID", SIZE:4,
                   'DEFAULT':'blam',
                   0:{ 'NAME':"Halo 1", 'VALUE':'blam' },
                   1:{ 'NAME':"Halo 2", 'VALUE':'!MLB' }}
               }

#Shared Enumerator options
Materials_List = {0:{GUI_NAME:"Dirt"},
                  1:{GUI_NAME:"Sand"},
                  2:{GUI_NAME:"Stone"},
                  3:{GUI_NAME:"Snow"},
                  4:{GUI_NAME:"Wood"},
                  5:{GUI_NAME:"Metal Hollow"},
                  6:{GUI_NAME:"Metal Thin"},
                  7:{GUI_NAME:"Metal Thick"},
                  8:{GUI_NAME:"Rubber"},
                  9:{GUI_NAME:"Glass"},
                  10:{GUI_NAME:"Force Field"},
                  11:{GUI_NAME:"Grunt"},
                  12:{GUI_NAME:"Hunter Armor"},
                  13:{GUI_NAME:"Hunter Skin"},
                  14:{GUI_NAME:"Elite"},
                  15:{GUI_NAME:"Jackal"},
                  16:{GUI_NAME:"Jackal Energy Shield"},
                  17:{GUI_NAME:"Engineer Skin"},
                  18:{GUI_NAME:"Engineer Force Field"},
                  19:{GUI_NAME:"Flood Combat Form"},
                  20:{GUI_NAME:"Flood Carrier Form"},
                  21:{GUI_NAME:"Cyborg Armor"},
                  22:{GUI_NAME:"Cyborg Energy Shield"},
                  23:{GUI_NAME:"Human Armor"},
                  24:{GUI_NAME:"Human Skin"},
                  25:{GUI_NAME:"Sentinel"},
                  26:{GUI_NAME:"Moniter"},
                  27:{GUI_NAME:"Plastic"},
                  28:{GUI_NAME:"Water"},
                  29:{GUI_NAME:"Leaves"},
                  30:{GUI_NAME:"Elite Energy Shield"},
                  31:{GUI_NAME:"Ice"},
                  32:{GUI_NAME:"Hunter Shield"}
                  }


#Transparent Shader Shared Functions

Transparent_Shader_Properties = {0:{GUI_NAME:"Alpha Tested"},
                                 1:{GUI_NAME:"Decal"},
                                 2:{GUI_NAME:"Two Sided"},
                                 3:{GUI_NAME:"First Map is in Screenspace"},
                                 4:{GUI_NAME:"Draw Before Water"},
                                 5:{GUI_NAME:"Ignore Effect"},
                                 6:{GUI_NAME:"Scale First Map With Distance"},
                                 7:{GUI_NAME:"Numeric"}
                                 }
Transparent_Shader_Fade_Mode = {0:{GUI_NAME:"None"},
                                1:{GUI_NAME:"Fade when Perpendicular"},
                                2:{GUI_NAME:"Fade when Parallel"}
                                }
Transparent_Shader_First_Map_Type = {0:{GUI_NAME:"Map 2D"},
                                     1:{GUI_NAME:"Reflection Cube Map"},
                                     2:{GUI_NAME:"Object Centered Cube Map"},
                                     3:{GUI_NAME:"Viewer Centered Cube Map"}
                                     }


#Shared Functions

Animation_Functions = {0:{GUI_NAME:"One"},
                       1:{GUI_NAME:"Zero"},
                       2:{GUI_NAME:"Cosine"},
                       3:{GUI_NAME:"Cosine Variable Period"},
                       4:{GUI_NAME:"Diagonal Wave"},
                       5:{GUI_NAME:"Diagonal Wave Variable Period"},
                       6:{GUI_NAME:"Slide"},
                       7:{GUI_NAME:"Slide Variable Period"},
                       8:{GUI_NAME:"Noise"},
                       9:{GUI_NAME:"Jitter"},
                       10:{GUI_NAME:"Wander"},
                       11:{GUI_NAME:"Spark"}
                       }
Detail_Map_Functions = {0:{GUI_NAME:"Double/Biased Multiply"},
                        1:{GUI_NAME:"Multiply"},
                        2:{GUI_NAME:"Double/Biased Add"}
                        }
Blend_Functions = { 0:{GUI_NAME:"Current"},
                    1:{GUI_NAME:"Next Map"},
                    2:{GUI_NAME:"Multiply"},
                    3:{GUI_NAME:"Double Multiply"},
                    4:{GUI_NAME:"Add"},
                    5:{GUI_NAME:"Add-Signed Current"},
                    6:{GUI_NAME:"Add-Signed Next Map"},
                    7:{GUI_NAME:"Subtract-Signed Current"},
                    8:{GUI_NAME:"Subtract-Signed Next Map"},
                    9:{GUI_NAME:"Blend Current Alpha"},
                    10:{GUI_NAME:"Blend Current Alpha-Inverse"},
                    11:{GUI_NAME:"Blend Next map Alpha"},
                    12:{GUI_NAME:"Blend Next map Alpha-Inverse"}
                    }
Framebuffer_Blend_Modes = {0:{GUI_NAME:"Alpha Blend"},
                           1:{GUI_NAME:"Multiply"},
                           2:{GUI_NAME:"Double Multiply"},
                           3:{GUI_NAME:"Add"},
                           4:{GUI_NAME:"Subtract"},
                           5:{GUI_NAME:"Component Min"},
                           6:{GUI_NAME:"Component Max"},
                           7:{GUI_NAME:"Alpha-Multiply Add"}
                           }
Function_Names = { 0:{GUI_NAME:"None"},
                   1:{GUI_NAME:"A"},
                   2:{GUI_NAME:"B"},
                   3:{GUI_NAME:"C"},
                   4:{GUI_NAME:"D"}
                   }
Function_Inputs = { 0:{GUI_NAME:"None"},
                    1:{GUI_NAME:"A In"},
                    2:{GUI_NAME:"B In"},
                    3:{GUI_NAME:"C In"},
                    4:{GUI_NAME:"D In"}
                    }
Function_Outputs = { 0:{GUI_NAME:"None"},
                     1:{GUI_NAME:"A Out"},
                     2:{GUI_NAME:"B Out"},
                     3:{GUI_NAME:"C Out"},
                     4:{GUI_NAME:"D Out"}
                     }

All_Shader_Enums = {0:{VALUE:"shdr", NAME:"shader"},
                    1:{VALUE:"senv", NAME:"shader_environment"},
                    2:{VALUE:"soso", NAME:"shader_model"},
                    3:{VALUE:"schi", NAME:"shader_transparent_chicago"},
                    4:{VALUE:"scex", NAME:"shader_transparent_chicago_extended"},
                    5:{VALUE:"sotr", NAME:"shader_transparent_generic"},
                    6:{VALUE:"sgla", NAME:"shader_transparent_glass"},
                    7:{VALUE:"smet", NAME:"shader_transparent_meter"},
                    8:{VALUE:"spla", NAME:"shader_transparent_plasma"},
                    9:{VALUE:"swat", NAME:"shader_transparent_water"}
                    }


#Miscellaneous blocks
Anim_Func_Per_Pha = {TYPE:Struct,
                     0:Com({TYPE:Enum16, OFFSET:0, GUI_NAME:"Function"},
                               Animation_Functions ),
                     1:{ TYPE:Float, OFFSET:4, GUI_NAME:"Period"},#seconds
                     2:{ TYPE:Float, OFFSET:8, GUI_NAME:"Phase"},#seconds
                     }

Anim_Src_Func_Per_Pha_Sca = {TYPE:Struct,
                            0:Com({TYPE:Enum16, OFFSET:0, GUI_NAME:"Source"},
                                  Function_Outputs ),
                            1:Com({TYPE:Enum16, OFFSET:2, GUI_NAME:"Function"},
                                  Animation_Functions ),
                            2:{ TYPE:Float, OFFSET:4, GUI_NAME:"Period"},#seconds
                            3:{ TYPE:Float, OFFSET:8, GUI_NAME:"Phase"},
                            4:{ TYPE:Float, OFFSET:12, GUI_NAME:"Scale"}#repeats
                            }


#This is the structure for all points where a tag references a chunk of raw data
Raw_Data_Reference_Structure = { TYPE:Struct, GUI_NAME:'Halo Raw Data Ref',
                                 0:{ TYPE:UInt32, GUI_NAME:"Byte Count",     EDITABLE:False },
                                 1:{ TYPE:UInt32, GUI_NAME:"Data_Unknown_1", EDITABLE:False },
                                 2:{ TYPE:UInt32, GUI_NAME:"Data_Unknown_2", EDITABLE:False },
                                 3:{ TYPE:UInt32, GUI_NAME:"Data_Unknown_3", EDITABLE:False },
                                 4:{ TYPE:UInt32, GUI_NAME:"Data_Unknown_4", EDITABLE:False }
                                 }

#This is the structure for all points where a tag references a block
Block_Reference_Structure = { TYPE:Struct, GUI_NAME:'Halo Block Ref',
                              0:{ TYPE:UInt32, GUI_NAME:"Block Count",   EDITABLE:False },
                              1:{ TYPE:UInt32, GUI_NAME:"Block ID",      EDITABLE:False },
                              2:{ TYPE:UInt32, GUI_NAME:"Block Type ID", EDITABLE:False }
                              }

#This is the structure for all points where a tag references another tag
Tag_Reference_Structure = { TYPE:Struct, GUI_NAME:'Halo Tag Ref',
                            0:Com({TYPE:Str_Latin1_Enum, GUI_NAME:"Tag Class",
                                   SIZE:4, EDITABLE:False}, All_Tag_Enums),
                            1:{ TYPE:UInt32, GUI_NAME:"Tag Path Pointer", EDITABLE:False },
                            2:{ TYPE:UInt32, GUI_NAME:"Tag Path Length", EDITABLE:False },
                            3:{ TYPE:SInt32, GUI_NAME:"Tag ID", EDITABLE:False, DEFAULT:-1},
                            CHILD:{TYPE:String_Var_Len, NAME:"Filepath", SIZE:Tag_Ref_Size}
                            }



"""Shader Stuff"""

Material_Type = Com({ TYPE:Enum16, OFFSET:34, GUI_NAME:"Material Type"}, Materials_List )

#THIS FIELD IS OFTEN INCORRECT ON STOCK TAGS
#This means it likely doesn't matter, but lets not take that chance
Numeric_Shader_ID = { TYPE:Enum8, OFFSET:36, GUI_NAME:"Numeric Shader ID", EDITABLE:False ,
                      0:{NAME:"SHDR", VALUE:255},#NOT TESTED, Guessed at
                      1:{NAME:"SENV", VALUE:3},#Environment
                      2:{NAME:"SOSO", VALUE:4},#Model
                      3:{NAME:"SOTR", VALUE:5},#Transparent Generic
                      4:{NAME:"SCHI", VALUE:6},#Transparent Chicago
                      5:{NAME:"SCEX", VALUE:7},#Transparent Chicago Extended
                      6:{NAME:"SWAT", VALUE:8},#Water
                      7:{NAME:"SGLA", VALUE:9},#Glass
                      8:{NAME:"SMET", VALUE:10},#Meter
                      9:{NAME:"SPLA", VALUE:11}#Plasma
                      }


"""Radiosity Stuff"""

Radiosity_Block = {TYPE:Struct, OFFSET:0, GUI_NAME:"Radiosity Settings",
                   0:{ TYPE:Bool16, OFFSET:0, GUI_NAME:"Radiosity Flags",
                       0:{GUI_NAME:"Simple Parameterization"},
                       1:{GUI_NAME:"Ignore Normals"},
                       2:{GUI_NAME:"Transparent Lit"}
                       },
                   1:{ TYPE:Enum16, OFFSET:2, GUI_NAME:"Radiosity Detail Level" ,
                       0:{GUI_NAME:"High"},
                       1:{GUI_NAME:"Medium"},
                       2:{GUI_NAME:"Low"},
                       3:{GUI_NAME:"Turd"}
                       },
                   2:{TYPE:Float, OFFSET:4, GUI_NAME:"Radiosity Light Power"},
                   3:Com({OFFSET:8, GUI_NAME:"Radiosity Light Color"}, R_G_B_Float),
                   4:Com({OFFSET:20, GUI_NAME:"Radiosity Tint Color"}, R_G_B_Float)
                   }


#Transparent Shader Stuff

Extra_Layers_Block = {TYPE:Struct, GUI_NAME:"Extra Layer",
                      ATTRS:Tag_Reference_Structure,
                      0:Com( {TYPE:Str_Latin1_Enum, GUI_NAME:"Tag Class",
                             SIZE:4}, All_Shader_Enums )
                      }

Chicago_4_Stage_Maps = {TYPE:Struct, SIZE:220, GUI_NAME:"Four Stage Map",
                        0:{ TYPE:Bool16, OFFSET:0, GUI_NAME:"Flags" ,
                            0:{GUI_NAME:"Unfiltered"},
                            1:{GUI_NAME:"Alpha Replicate"},
                            2:{GUI_NAME:"U-Clamped"},
                            3:{GUI_NAME:"V-Clamped"}
                            },
                        1:Com({TYPE:Enum16, OFFSET:44, GUI_NAME:"Color Function"},
                              Blend_Functions ),
                        2:Com({TYPE:Enum16, OFFSET:46, GUI_NAME:"Alpha Function Function"},
                              Blend_Functions ),
                        #shader transformations
                        3:{ TYPE:Float, OFFSET:84, GUI_NAME:"Map U-Scale" },
                        4:{ TYPE:Float, OFFSET:88, GUI_NAME:"Map V-Scale" },
                        5:{ TYPE:Float, OFFSET:92, GUI_NAME:"Map U-Offset" },
                        6:{ TYPE:Float, OFFSET:96, GUI_NAME:"Map V-Offset" },
                        7:{ TYPE:Float, OFFSET:100, GUI_NAME:"Map Rotation"},#degrees
                        8:{ TYPE:Float, OFFSET:104, GUI_NAME:"Map Bias"},#[0,1]
                        9: {TYPE:Struct, OFFSET:108, GUI_NAME:"Bitmap" ,
                            ATTRS:Tag_Reference_Structure },

                        #shader animations
                        10:{TYPE:Struct, OFFSET:164, GUI_NAME:"U-Animation",
                            ATTRS:Anim_Src_Func_Per_Pha_Sca },
                        
                        11:{TYPE:Struct, OFFSET:180, GUI_NAME:"V-Animation",
                            ATTRS:Anim_Src_Func_Per_Pha_Sca },
                        
                        12:{TYPE:Struct, OFFSET:196, GUI_NAME:"Rotation-Animation",
                            ATTRS:Anim_Src_Func_Per_Pha_Sca,
                            4:{ TYPE:Float, OFFSET:12, GUI_NAME:"Scale"}#degrees
                            },
                        13:Com({OFFSET:212, GUI_NAME:"Rotation Center"}, X_Y_Float)
                        }


Chicago_2_Stage_Maps = Com({GUI_NAME:"Two Stage Map"}, Chicago_4_Stage_Maps)

Chicago_Extra_Flags = {0:{GUI_NAME:"Dont Fade Active Camouflage"},
                       1:{GUI_NAME:"Numeric Countdown Timer"}
                       }
