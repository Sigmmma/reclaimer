from copy import copy
from supyr_struct.defs.common_descriptors import *
from .fields import *
from .constants import *

com = combine


All_Valid_Tags = { 0:{VALUE:'actr', NAME:"actor"},
                   1:{VALUE:'actv', NAME:"actor_varient"},
                   2:{VALUE:'ant!', NAME:"antenna"},
                   3:{VALUE:'bipd', NAME:"biped"},
                   4:{VALUE:'bitm', NAME:"bitmap"},
                   5:{VALUE:'trak', NAME:"camera_track"},
                   6:{VALUE:'colo', NAME:"color_table"},
                   7:{VALUE:'cdmg', NAME:"continuous_damage_effect"},
                   8:{VALUE:'cont', NAME:"contrail"},
                   9:{VALUE:'jpt!', NAME:"damage_effect"},
                   10:{VALUE:'deca', NAME:"decal"},
                   11:{VALUE:'udlg', NAME:"dialogue"},
                   12:{VALUE:'dobc', NAME:"detail_object_collection"},
                   13:{VALUE:'devi', NAME:"device"},
                   14:{VALUE:'ctrl', NAME:"device_control"},
                   15:{VALUE:'lifi', NAME:"device_light_fixture"},
                   16:{VALUE:'mach', NAME:"device_machine"},
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
                   82:{VALUE:'wind', NAME:"wind"},

                   83:{VALUE:0xffffffff, NAME:"None"}
                   }


All_Valid_Attachments = { 0:{VALUE:'cont', NAME:"contrail"},
                          1:{VALUE:'effe', NAME:"effect"},
                          2:{VALUE:'ligh', NAME:"light"},
                          3:{VALUE:'mgs2', NAME:"light_volume"},
                          4:{VALUE:'pctl', NAME:"particle_system"},
                          5:{VALUE:'lsnd', NAME:"sound_looping"},

                          6:{VALUE:0xffffffff, NAME:"None"}
                          }

All_Valid_Effect_Events = { 0:{VALUE:'bipd', NAME:"biped"},
                            1:{VALUE:'jpt!', NAME:"damage_effect"},
                            2:{VALUE:'deca', NAME:"decal"},
                            3:{VALUE:'devi', NAME:"device"},
                            4:{VALUE:'ctrl', NAME:"device_control"},
                            5:{VALUE:'lifi', NAME:"device_light_fixture"},
                            6:{VALUE:'mach', NAME:"device_machine"},
                            7:{VALUE:'eqip', NAME:"equipment"},
                            8:{VALUE:'garb', NAME:"garbage"},
                            9:{VALUE:'item', NAME:"item"},
                            10:{VALUE:'ligh', NAME:"light"},
                            11:{VALUE:'obje', NAME:"object"},
                            12:{VALUE:'pctl', NAME:"particle_system"},
                            13:{VALUE:'plac', NAME:"placeholder"},
                            14:{VALUE:'proj', NAME:"projectile"},
                            15:{VALUE:'scen', NAME:"scenery"},
                            16:{VALUE:'snd!', NAME:"sound"},
                            17:{VALUE:'ssce', NAME:"sound_scenery"},
                            18:{VALUE:'unit', NAME:"unit"},
                            19:{VALUE:'vehi', NAME:"vehicle"},
                            20:{VALUE:'weap', NAME:"weapon"},
                            21:{VALUE:0xffffffff, NAME:"None"}
                            }

All_Valid_Effects = {0:{VALUE:'snd!',     NAME:"sound"},
                     1:{VALUE:'effe',     NAME:"effect"},
                     2:{VALUE:0xffffffff, NAME:"None"}
                     }

All_Valid_Items = { 0:{VALUE:'eqip', NAME:"equipment"},
                    1:{VALUE:'garb', NAME:"garbage"},
                    2:{VALUE:'item', NAME:"item"},
                    3:{VALUE:'weap', NAME:"weapon"},
                    4:{VALUE:0xffffffff, NAME:"None"}
                    }

All_Valid_Objects = { 0:{VALUE:'bipd', NAME:"biped"},
                      1:{VALUE:'devi', NAME:"device"},
                      2:{VALUE:'ctrl', NAME:"device_control"},
                      3:{VALUE:'lifi', NAME:"device_light_fixture"},
                      4:{VALUE:'mach', NAME:"device_machine"},
                      5:{VALUE:'eqip', NAME:"equipment"},
                      6:{VALUE:'obje', NAME:"object"},
                      7:{VALUE:'proj', NAME:"projectile"},
                      8:{VALUE:'scen', NAME:"scenery"},
                      9:{VALUE:'ssce', NAME:"sound_scenery"},
                      10:{VALUE:'vehi', NAME:"vehicle"},
                      11:{VALUE:'weap', NAME:"weapon"},
                      12:{VALUE:0xffffffff, NAME:"None"}
                      }


All_Valid_Shaders = { 0:{VALUE:'shdr', NAME:"shader"},
                      1:{VALUE:'schi', NAME:"shader_transparent_chicago"},
                      2:{VALUE:'scex', NAME:"shader_transparent_chicago_extended"},
                      3:{VALUE:'sotr', NAME:"shader_transparent_generic"},
                      4:{VALUE:'senv', NAME:"shader_environment"},
                      5:{VALUE:'sgla', NAME:"shader_transparent_glass"},
                      6:{VALUE:'smet', NAME:"shader_transparent_meter"},
                      7:{VALUE:'soso', NAME:"shader_model"},
                      8:{VALUE:'spla', NAME:"shader_transparent_plasma"},
                      9:{VALUE:'swat', NAME:"shader_transparent_water"},
                      10:{VALUE:0xffffffff, NAME:"None"}
                      }

All_Valid_Units = { 0:{VALUE:'bipd', NAME:"biped"},
                    1:{VALUE:'unit', NAME:"unit"},
                    2:{VALUE:'vehi', NAME:"vehicle"}
                    }

All_Valid_Widgets = { 0:{VALUE:'ant!', NAME:"antenna"},
                      1:{VALUE:'flag', NAME:"flag"},
                      2:{VALUE:'glw!', NAME:"glow"},
                      3:{VALUE:'mgs2', NAME:"light_volume"},
                      4:{VALUE:'elec', NAME:"lightning"},

                      5:{VALUE:0xffffffff, NAME:"None"}
                      }

#Enumerators for different types of tag references
Tag_Class = { TYPE:Enum32, NAME:"Tag_Class", DEFAULT:0xffffffff }

Tag_Header = { TYPE:Struct, SIZE:64, NAME:"Blam_Header", EDITABLE:False,
               0:{ TYPE:Pad, SIZE:36 },
               1:com({}, Tag_Class, All_Valid_Tags),
               2:{ TYPE:UInt32, NAME:"Base_Address", DEFAULT:0 },#random
               3:{ TYPE:UInt32, NAME:"Header_Size",  DEFAULT:64 },
               4:{ TYPE:Pad, SIZE:8 },
               5:{ TYPE:UInt16, NAME:"Version", DEFAULT:1 },
               6:{ TYPE:UInt16, NAME:"Unknown", DEFAULT:255 },
               7:{ TYPE:Enum32, NAME:"Engine_ID",
                   DEFAULT:'blam',
                   0:{ 'NAME':"Halo 1", 'VALUE':'blam' },
                   1:{ 'NAME':"Halo 2", 'VALUE':'BLM!' }
                   }
               }

#Shared Enumerator options
Materials_List = {0:{GUI_NAME:"Dirt"},
                  1:{GUI_NAME:"Sand"},
                  2:{GUI_NAME:"Stone"},
                  3:{GUI_NAME:"Snow"},
                  4:{GUI_NAME:"Wood"},
                  5:{GUI_NAME:"Metal hollow"},
                  6:{GUI_NAME:"Metal thin"},
                  7:{GUI_NAME:"Metal thick"},
                  8:{GUI_NAME:"Rubber"},
                  9:{GUI_NAME:"Glass"},
                  10:{GUI_NAME:"Force field"},
                  11:{GUI_NAME:"Grunt"},
                  12:{GUI_NAME:"Hunter armor"},
                  13:{GUI_NAME:"Hunter skin"},
                  14:{GUI_NAME:"Elite"},
                  15:{GUI_NAME:"Jackal"},
                  16:{GUI_NAME:"Jackal energy shield"},
                  17:{GUI_NAME:"Engineer skin"},
                  18:{GUI_NAME:"Engineer force field"},
                  19:{GUI_NAME:"Flood combat form"},
                  20:{GUI_NAME:"Flood carrier form"},
                  21:{GUI_NAME:"Cyborg armor"},
                  22:{GUI_NAME:"Cyborg energy shield"},
                  23:{GUI_NAME:"Human armor"},
                  24:{GUI_NAME:"Human skin"},
                  25:{GUI_NAME:"Sentinel"},
                  26:{GUI_NAME:"Moniter"},
                  27:{GUI_NAME:"Plastic"},
                  28:{GUI_NAME:"Water"},
                  29:{GUI_NAME:"Leaves"},
                  30:{GUI_NAME:"Elite energy shield"},
                  31:{GUI_NAME:"Ice"},
                  32:{GUI_NAME:"Hunter shield"}
                  }


#Transparent Shader Shared Functions

Transparent_Shader_Properties = {0:{GUI_NAME:"Alpha tested"},
                                 1:{GUI_NAME:"Decal"},
                                 2:{GUI_NAME:"Two sided"},
                                 3:{GUI_NAME:"First map is in screenspace"},
                                 4:{GUI_NAME:"Draw before water"},
                                 5:{GUI_NAME:"Ignore effect"},
                                 6:{GUI_NAME:"Scale first map with distance"},
                                 7:{GUI_NAME:"Numeric"}
                                 }
Transparent_Shader_Fade_Mode = {0:{GUI_NAME:"None"},
                                1:{GUI_NAME:"Fade when perpendicular"},
                                2:{GUI_NAME:"Fade when parallel"}
                                }
Transparent_Shader_First_Map_Type = {0:{GUI_NAME:"Map 2D"},
                                     1:{GUI_NAME:"Reflection cube map"},
                                     2:{GUI_NAME:"Object centered cube map"},
                                     3:{GUI_NAME:"Viewer centered cube map"}
                                     }


#Shared Functions

Animation_Functions = {0:{GUI_NAME:"One"},
                       1:{GUI_NAME:"Zero"},
                       2:{GUI_NAME:"Cosine"},
                       3:{GUI_NAME:"Cosine variable period"},
                       4:{GUI_NAME:"Diagonal wave"},
                       5:{GUI_NAME:"Diagonal wave variable period"},
                       6:{GUI_NAME:"Slide"},
                       7:{GUI_NAME:"Slide variable period"},
                       8:{GUI_NAME:"Noise"},
                       9:{GUI_NAME:"Jitter"},
                       10:{GUI_NAME:"Wander"},
                       11:{GUI_NAME:"Spark"}
                       }
Detail_Map_Functions = {0:{GUI_NAME:"Double/biased multiply"},
                        1:{GUI_NAME:"Multiply"},
                        2:{GUI_NAME:"Double/biased add"}
                        }
Device_Functions = {0:{GUI_NAME:"None"},
                    1:{GUI_NAME:"Power"},
                    2:{GUI_NAME:"Change in power"},
                    3:{GUI_NAME:"Position"},
                    4:{GUI_NAME:"Change in position"},
                    5:{GUI_NAME:"Locked"},
                    6:{GUI_NAME:"Delay"},
                    }
Blend_Functions = { 0:{GUI_NAME:"Current"},
                    1:{GUI_NAME:"Next map"},
                    2:{GUI_NAME:"Multiply"},
                    3:{GUI_NAME:"Double multiply"},
                    4:{GUI_NAME:"Add"},
                    5:{GUI_NAME:"Add-signed current"},
                    6:{GUI_NAME:"Add-signed next map"},
                    7:{GUI_NAME:"Subtract-signed current"},
                    8:{GUI_NAME:"Subtract-signed next map"},
                    9:{GUI_NAME:"Blend current alpha"},
                    10:{GUI_NAME:"Blend current alpha-inverse"},
                    11:{GUI_NAME:"Blend next map alpha"},
                    12:{GUI_NAME:"Blend next map alpha-inverse"}
                    }
Framebuffer_Blend_Modes = {0:{GUI_NAME:"Alpha blend"},
                           1:{GUI_NAME:"Multiply"},
                           2:{GUI_NAME:"Double multiply"},
                           3:{GUI_NAME:"Add"},
                           4:{GUI_NAME:"Subtract"},
                           5:{GUI_NAME:"Component min"},
                           6:{GUI_NAME:"Component max"},
                           7:{GUI_NAME:"Alpha-multiply add"}
                           }
Function_Names = { 0:{GUI_NAME:"None"},
                   1:{GUI_NAME:"A"},
                   2:{GUI_NAME:"B"},
                   3:{GUI_NAME:"C"},
                   4:{GUI_NAME:"D"}
                   }
Function_Inputs = { 0:{GUI_NAME:"None"},
                    1:{GUI_NAME:"A in"},
                    2:{GUI_NAME:"B in"},
                    3:{GUI_NAME:"C in"},
                    4:{GUI_NAME:"D in"}
                    }
Function_Outputs = { 0:{GUI_NAME:"None"},
                     1:{GUI_NAME:"A out"},
                     2:{GUI_NAME:"B out"},
                     3:{GUI_NAME:"C out"},
                     4:{GUI_NAME:"D out"}
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
                     0:com({TYPE:Enum16, OFFSET:0, GUI_NAME:"Function"},
                               Animation_Functions ),
                     1:{ TYPE:Float, OFFSET:4, GUI_NAME:"Period"},#seconds
                     2:{ TYPE:Float, OFFSET:8, GUI_NAME:"Phase"},#seconds
                     }

Anim_Src_Func_Per_Pha_Sca = {TYPE:Struct,
                            0:com({TYPE:Enum16, OFFSET:0, GUI_NAME:"Source"},
                                  Function_Outputs ),
                            1:com({TYPE:Enum16, OFFSET:2, GUI_NAME:"Function"},
                                  Animation_Functions ),
                            2:{ TYPE:Float, OFFSET:4, GUI_NAME:"Period"},#seconds
                            3:{ TYPE:Float, OFFSET:8, GUI_NAME:"Phase"},
                            4:{ TYPE:Float, OFFSET:12, GUI_NAME:"Scale"}#repeats
                            }

From_To = { TYPE:Struct,
            0:{ TYPE:Float, GUI_NAME:" ", NAME:"From" },
            1:{ TYPE:Float, NAME:"To" },
            }


#This is the structure for all points where a tag references a chunk of raw data
Raw_Data_Ref_Struct = { TYPE:RawDataRef, GUI_NAME:'Raw Data Ref', EDITABLE:False,
                        0:{ TYPE:SInt32, NAME:"Count" },
                        1:{ TYPE:SInt32, NAME:"Unknown_1" },#0x00000000 in tags
                        2:{ TYPE:SInt32, NAME:"Unknown_2" },#random
                        3:{ TYPE:SInt32, NAME:"Unknown_3" },#random
                        4:{ TYPE:UInt32, NAME:"ID" },#random
                        }

#This is the structure for all tag reflexives
Reflexive_Struct = { TYPE:Reflexive, GUI_NAME:'Reflexive', EDITABLE:False,
                     0:{ TYPE:SInt32, NAME:"Count" },
                     1:{ TYPE:SInt32, NAME:"ID" },#random
                     2:{ TYPE:UInt32, NAME:"Reflexive_ID" }#random
                     }

#This is the structure for all points where a tag references another tag
Tag_Index_Ref_Struct = { TYPE:TagIndexRef, GUI_NAME:'TagIndexRef', EDITABLE:False,
                         0:com( {}, Tag_Class, All_Valid_Tags),
                         1:{ TYPE:SInt32, NAME:"Tag_Path_Pointer" },#random
                         2:{ TYPE:SInt32, NAME:"Tag_Path_Length" },
                         3:{ TYPE:UInt32, NAME:"Tag_ID", DEFAULT:0xFFFFFFFF },#random
                         CHILD:{TYPE:StringVarLen, NAME:"Filepath", SIZE:tag_ref_size}
                         }
                         
Ref_Struct = copy(Tag_Index_Ref_Struct)
del Ref_Struct[0]

Attachment_Ref_Struct   = com( {0:com( {}, Tag_Class, All_Valid_Attachments)},   Ref_Struct)
Effect_Ref_Struct       = com( {0:com( {}, Tag_Class, All_Valid_Effects)},       Ref_Struct)
Effect_Event_Ref_Struct = com( {0:com( {}, Tag_Class, All_Valid_Effect_Events)}, Ref_Struct)
Item_Ref_Struct         = com( {0:com( {}, Tag_Class, All_Valid_Items)},         Ref_Struct)
Object_Ref_Struct       = com( {0:com( {}, Tag_Class, All_Valid_Objects)},       Ref_Struct)
Shader_Ref_Struct       = com( {0:com( {}, Tag_Class, All_Valid_Shaders)},       Ref_Struct)
Unit_Ref_Struct         = com( {0:com( {}, Tag_Class, All_Valid_Units)},         Ref_Struct)
Widget_Ref_Struct       = com( {0:com( {}, Tag_Class, All_Valid_Widgets)},       Ref_Struct)
Shader_Ref_Struct       = com( {0:com( {}, Tag_Class, All_Shader_Enums)},        Ref_Struct)

del Ref_Struct


"""Shader Stuff"""

Material_Type = com({ TYPE:Enum16, OFFSET:34, GUI_NAME:"Material Type"}, Materials_List )

#THIS FIELD IS OFTEN INCORRECT ON STOCK TAGS
#This means it likely doesn't matter, but lets not take that chance
Numeric_Shader_ID = { TYPE:FlEnum16, GUI_NAME:"Numeric Shader ID",
                      OFFSET:36, EDITABLE:False,
                      0:{NAME:"shdr", VALUE:0xffff},#NOT TESTED, Guessed at
                      1:{NAME:"senv", VALUE:3},#Environment
                      2:{NAME:"soso", VALUE:4},#Model
                      3:{NAME:"sotr", VALUE:5},#Transparent Generic
                      4:{NAME:"schi", VALUE:6},#Transparent Chicago
                      5:{NAME:"scex", VALUE:7},#Transparent Chicago Extended
                      6:{NAME:"swat", VALUE:8},#Water
                      7:{NAME:"sgla", VALUE:9},#Glass
                      8:{NAME:"smet", VALUE:10},#Meter
                      9:{NAME:"spla", VALUE:11}#Plasma
                      }


"""Radiosity Stuff"""

Radiosity_Block = {TYPE:Struct, OFFSET:0, GUI_NAME:"Radiosity Settings",
                   0:{ TYPE:Bool16, OFFSET:0, GUI_NAME:"Radiosity Flags",
                       0:{GUI_NAME:"Simple parameterization"},
                       1:{GUI_NAME:"Ignore normals"},
                       2:{GUI_NAME:"Transparent lit"}
                       },
                   1:{ TYPE:Enum16, OFFSET:2, GUI_NAME:"Radiosity Detail Level" ,
                       0:{GUI_NAME:"High"},
                       1:{GUI_NAME:"Medium"},
                       2:{GUI_NAME:"Low"},
                       3:{GUI_NAME:"Turd"}
                       },
                   2:{TYPE:Float, OFFSET:4, GUI_NAME:"Radiosity Light Power"},
                   3:com({OFFSET:8, GUI_NAME:"Radiosity Light Color"}, R_G_B_Float),
                   4:com({OFFSET:20, GUI_NAME:"Radiosity Tint Color"}, R_G_B_Float)
                   }


#Transparent Shader Stuff

Extra_Layers_Block = com({TYPE:TagIndexRef, GUI_NAME:"Extra Layer"}, Shader_Ref_Struct )

Chicago_4_Stage_Maps = {TYPE:Struct, SIZE:220, GUI_NAME:"Four Stage Map",
                        0:{ TYPE:Bool16, OFFSET:0, GUI_NAME:"Flags" ,
                            0:{GUI_NAME:"Unfiltered"},
                            1:{GUI_NAME:"Alpha replicate"},
                            2:{GUI_NAME:"U-clamped"},
                            3:{GUI_NAME:"V-clamped"}
                            },
                        1:com({TYPE:Enum16, OFFSET:44, GUI_NAME:"Color Function"},
                               Blend_Functions ),
                        2:com({TYPE:Enum16, OFFSET:46, GUI_NAME:"Alpha Function Function"},
                               Blend_Functions ),
                        #shader transformations
                        3:{ TYPE:Float, OFFSET:84, GUI_NAME:"Map U-Scale" },
                        4:{ TYPE:Float, OFFSET:88, GUI_NAME:"Map V-Scale" },
                        5:{ TYPE:Float, OFFSET:92, GUI_NAME:"Map U-Offset" },
                        6:{ TYPE:Float, OFFSET:96, GUI_NAME:"Map V-Offset" },
                        7:{ TYPE:Float, OFFSET:100, GUI_NAME:"Map Rotation"},#degrees
                        8:{ TYPE:Float, OFFSET:104, GUI_NAME:"Map Bias"},#[0,1]
                        9: {TYPE:TagIndexRef, OFFSET:108, GUI_NAME:"Bitmap" ,
                            INCLUDE:Tag_Index_Ref_Struct },

                        #shader animations
                        10:{TYPE:Struct, OFFSET:164, GUI_NAME:"U-Animation",
                            INCLUDE:Anim_Src_Func_Per_Pha_Sca },
                        
                        11:{TYPE:Struct, OFFSET:180, GUI_NAME:"V-Animation",
                            INCLUDE:Anim_Src_Func_Per_Pha_Sca },
                        
                        12:{TYPE:Struct, OFFSET:196, GUI_NAME:"Rotation-Animation",
                            INCLUDE:Anim_Src_Func_Per_Pha_Sca,
                            4:{ TYPE:Float, OFFSET:12, GUI_NAME:"Scale"}#degrees
                            },
                        13:com({OFFSET:212, GUI_NAME:"Rotation Center"}, X_Y_Float)
                        }


Chicago_2_Stage_Maps = com({GUI_NAME:"Two Stage Map"}, Chicago_4_Stage_Maps)

Chicago_Extra_Flags = {0:{GUI_NAME:"Dont fade active camouflage"},
                       1:{GUI_NAME:"Numeric countdown timer"}
                       }
