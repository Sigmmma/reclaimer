from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return AntrDef

class AntrDef(TagDef):

    ext = ".model_animations"

    def_id = "antr"

    endian = ">"

    object_desc = { TYPE:Struct, NAME:"object", SIZE:20,
                    0:{ TYPE:SInt16, NAME:"animation" },
                    1:{ TYPE:UInt16, NAME:"function" },
                    2:{ TYPE:UInt16, NAME:"function_controls" },
                    }

    anim_enum_desc = { TYPE:Struct, NAME:"animation",
                       0:{ TYPE:SInt16, NAME:"animation" }
                       }

    ik_point_desc = { TYPE:Struct, NAME:"ik_point", SIZE:64,
                      0:{ TYPE:StrLatin1, NAME:"marker", SIZE:32 },
                      1:{ TYPE:StrLatin1, NAME:"attach_to_marker", SIZE:32 }
                      }

    weapon_types_desc = { TYPE:Struct, NAME:"weapon_types", SIZE:60,
                          0:{ TYPE:StrLatin1, NAME:"label", SIZE:32 },
                          1:{ TYPE:Pad, SIZE:16 },
                          2:{ TYPE:Reflexive, NAME:"animations",
                              INCLUDE:Reflexive_Struct, MAX:10,
                              CHILD:{ TYPE:Array, NAME:"animations_array",
                                      SUB_STRUCT:anim_enum_desc, SIZE:".Count"
                                      }
                              },
                          }

    unit_weapon_desc = { TYPE:Struct, NAME:"weapon", SIZE:188,
                         0:{ TYPE:StrLatin1, NAME:"name", SIZE:32 },
                         1:{ TYPE:StrLatin1, NAME:"grip marker", SIZE:32 },
                         2:{ TYPE:StrLatin1, NAME:"hand marker", SIZE:32 },
                         #Aiming screen bounds
                         
                         #pitch and yaw are saved in radians.
                         3:{ TYPE:Float,  NAME:"right_yaw_per_frame" },
                         4:{ TYPE:Float,  NAME:"left_yaw_per_frame" },
                         5:{ TYPE:SInt16, NAME:"right_frame_count" },
                         6:{ TYPE:SInt16, NAME:"left_frame_count" },
                      
                         7:{ TYPE:Float,  NAME:"down_pitch_per_frame" },
                         8:{ TYPE:Float,  NAME:"up_pitch_per_frame" },
                         9:{ TYPE:SInt16, NAME:"down_frame_count" },
                         10:{ TYPE:SInt16, NAME:"up_frame_count" },

                         11:{ TYPE:Pad, SIZE:32 },
                         12:{ TYPE:Reflexive, NAME:"animations",
                              #animations are as follows:
                              #0-1   == idle, gesture
                              #2-3   == turn-left/right
                              #4-7   == dive-front/back/left/right
                              #8-11  == move-front/back/left/right
                              #12-15 == slide-front/back/left/right
                              #16 == airborne
                              #17-18 == land-soft/hard
                              #19-24 == unused, throw-grenade, disarm, drop, ready, put-away
                              #25-26 == aim-still/move
                              #27-28 == surprise-front/back
                              #29 == berserk
                              #30-31 == evade-left/right
                              #32-33 == signal-move/attack
                              #34 == warn
                              #35-38 == stunned-front/back/left/right
                              #39-43 == melee, celebrate, panic, melee-airborne, flaming
                              #44-45 == resurrect-front/back
                              #46 == melee-continuous
                              #47 == feeding
                              #48-50 == leap-start/airborne/melee
                              #51-54 == zapping, unused, unused, unused
                              INCLUDE:Reflexive_Struct,
                              CHILD:{ TYPE:Array, NAME:"animations_array",
                                      SUB_STRUCT:anim_enum_desc,
                                      SIZE:".Count", MAX:55
                                      }
                              },
                         13:{ TYPE:Reflexive, NAME:"ik_points",
                              INCLUDE:Reflexive_Struct,
                              CHILD:{ TYPE:Array, NAME:"ik_points_array",
                                      SUB_STRUCT:ik_point_desc,
                                      SIZE:".Count", MAX:4
                                      }
                              },
                         14:{ TYPE:Reflexive, NAME:"weapon_types",
                              INCLUDE:Reflexive_Struct,
                              #animations are as follows:
                              #0-1 == reload-1, reload-2
                              #2-3 == chamber-1, chamber-2
                              #4-5 == fire-1, fire-2
                              #6-7 == charged-1, charged-2
                              #8-9 == melee, overheat
                              CHILD:{ TYPE:Array, NAME:"weapon_types_array",
                                      SUB_STRUCT:weapon_types_desc,
                                      SIZE:".Count", MAX:10
                                      }
                              }
                         }
    
    unit_desc = { TYPE:Struct, NAME:"unit", SIZE:100,
                  0:{ TYPE:StrLatin1, NAME:"label", SIZE:32 },
                  #Looking screen bounds
                  
                  #pitch and yaw are saved in radians.
                  1:{ TYPE:Float,  NAME:"right_yaw_per_frame" },
                  2:{ TYPE:Float,  NAME:"left_yaw_per_frame" },
                  3:{ TYPE:SInt16, NAME:"right_frame_count" },
                  4:{ TYPE:SInt16, NAME:"left_frame_count" },
                  
                  5:{ TYPE:Float,  NAME:"down_pitch_per_frame" },
                  6:{ TYPE:Float,  NAME:"up_pitch_per_frame" },
                  7:{ TYPE:SInt16, NAME:"down_frame_count" },
                  8:{ TYPE:SInt16, NAME:"up_frame_count" },

                  9:{ TYPE:Pad, SIZE:8 },
                  10:{ TYPE:Reflexive, NAME:"animations",
                       #animations are as follows:
                       #0  == airborne-dead
                       #1  == landing-dead
                       #2  == acc-front-back
                       #3  == acc-left-right
                       #4  == acc-up-down
                       #5-10 == push, twist, enter, exit, look, talk
                       #11 == emotions
                       #12 == unused
                       #13-22 == user0 - user9
                       #23 == flying-front
                       #24 == flying-back
                       #25 == flying-left
                       #26 == flying-right
                       #27-29 == opening, closing, hovering
                       INCLUDE:Reflexive_Struct,
                       CHILD:{ TYPE:Array, NAME:"animations_array",
                               SUB_STRUCT:anim_enum_desc,
                               SIZE:".Count", MAX:30 }
                       },
                  11:{ TYPE:Reflexive, NAME:"ik_points",
                       INCLUDE:Reflexive_Struct,
                       CHILD:{ TYPE:Array, NAME:"ik_points_array",
                               SUB_STRUCT:ik_point_desc,
                               SIZE:".Count", MAX:4 }
                       },
                  12:{ TYPE:Reflexive, NAME:"weapons",
                       INCLUDE:Reflexive_Struct,
                       CHILD:{ TYPE:Array, NAME:"weapons_array",
                               SUB_STRUCT:unit_weapon_desc,
                               SIZE:".Count", MAX:16 }
                       },
                  }

    weapons_desc = { TYPE:Struct, NAME:"weapons", SIZE:28,
                     0:{ TYPE:Pad, SIZE:16 },
                     1:{ TYPE:Reflexive, NAME:"animations",
                         INCLUDE:Reflexive_Struct,
                         #animations are as follows:
                         #0-2  == idle, ready, put-away
                         #3-4  == reload-1, reload-2
                         #5-6  == chamber-1, chamber-2
                         #7-8  == charged-1, charged-2
                         #9-10 == fire-1, fire-2
                         CHILD:{ TYPE:Array, NAME:"animations_array",
                                 SUB_STRUCT:anim_enum_desc,
                                 SIZE:".Count", MAX:11
                                 }
                         },
                  }

    suspension_desc = { TYPE:Struct, NAME:"suspension_animation", SIZE:20,
                        0:{ TYPE:SInt16, NAME:"mass_point_index" },
                        1:{ TYPE:SInt16, NAME:"animation" },
                        2:{ TYPE:Float,  NAME:"full_extension_ground_depth" },
                        3:{ TYPE:Float,  NAME:"full_compression_ground_depth" },
                        }

    vehicle_desc = { TYPE:Struct, NAME:"vehicle_desc", SIZE:116,
                     #Steering screen bounds
                     
                     #pitch and yaw are saved in radians.
                     0:{ TYPE:Float,  NAME:"right_yaw_per_frame" },
                     1:{ TYPE:Float,  NAME:"left_yaw_per_frame" },
                     2:{ TYPE:SInt16, NAME:"right_frame_count" },
                     3:{ TYPE:SInt16, NAME:"left_frame_count" },
                     
                     4:{ TYPE:Float,  NAME:"down_pitch_per_frame" },
                     5:{ TYPE:Float,  NAME:"up_pitch_per_frame" },
                     6:{ TYPE:SInt16, NAME:"down_frame_count" },
                     7:{ TYPE:SInt16, NAME:"up_frame_count" },

                     8:{ TYPE:Pad, SIZE:68 },
                     9:{ TYPE:Reflexive, NAME:"animations",
                          #animations are as follows:
                          #0-1 == steering, roll
                          #2-3 == throttle, velocity
                          #4-5 == braking,  ground-speed
                          #6-7 == occupied, unoccupied
                          INCLUDE:Reflexive_Struct,
                          CHILD:{ TYPE:Array, NAME:"animations_array",
                                  SUB_STRUCT:anim_enum_desc,
                                  SIZE:".Count", MAX:8 }
                          },
                     10:{ TYPE:Reflexive, NAME:"suspension_animation",
                          INCLUDE:Reflexive_Struct,
                          CHILD:{ TYPE:Array, NAME:"suspensions_array",
                                  SUB_STRUCT:suspension_desc,
                                  SIZE:".Count", MAX:8 }
                          },
                     }

    device_desc = { TYPE:Struct, NAME:"device", SIZE:96,
                    0:{ TYPE:Pad, SIZE:84 },
                    1:{ TYPE:Reflexive, NAME:"animations",
                        #animations are as follows:
                        #0 == position
                        #1 == power
                        INCLUDE:Reflexive_Struct,
                        CHILD:{ TYPE:Array, NAME:"animations_array",
                                SUB_STRUCT:anim_enum_desc,
                                SIZE:".Count", MAX:2
                                }
                        },
                  }

    fp_animation_desc = { TYPE:Struct, NAME:"fp_animation", SIZE:28,
                          0:{ TYPE:Pad, SIZE:16 },
                          1:{ TYPE:Reflexive, NAME:"animations",
                              #animations are as follows:
                              #0-4   == idle, posing, fire-1, moving, overlays
                              #5-6   == light-off/on
                              #7-8   == reload-empty/full
                              #9-11  == overheated, ready, put-away
                              #12-14 == overcharged, melee, fire-2
                              #15-17 == overcharged-jitter, throw-grenade, ammunition
                              #18-19 == misfire-1/2
                              #20-22 == throw-overheated, overheating, overheating-again
                              #23-27 == enter, exit-empty, exit-full, o-h-exit, o-h-s-enter
                              INCLUDE:Reflexive_Struct,
                              CHILD:{ TYPE:Array, NAME:"animations_array",
                                      SUB_STRUCT:anim_enum_desc,
                                      SIZE:".Count", MAX:28
                                      }
                              },
                          }

    sound_reference_desc = { TYPE:Struct, NAME:"sound_reference", SIZE:20,
                             0:com({NAME:'sound'}, Sound_Ref_Struct),
                             1:{ TYPE:Pad, SIZE:4 }
                             }

    nodes_desc = { TYPE:Struct, NAME:"node", SIZE:64,
                   0:{ TYPE:StrLatin1, NAME:"name", SIZE:32 },
                   1:{ TYPE:SInt16, NAME:"next_sibling_node_index" },
                   2:{ TYPE:SInt16, NAME:"first_child_node_index" },
                   3:{ TYPE:SInt16, NAME:"parent_node_index" },
                   4:{ TYPE:Pad, SIZE:2 },
                   5:{ TYPE:Bool32, NAME:"node_joint_flags",
                       0:{ NAME:"compress_all_animations" },
                       1:{ NAME:"force_idle_compression" },
                       },
                   6:com( {NAME:"base_vector"},I_J_K_Float),
                   7:{ TYPE:Float, NAME:"vector_range" },
                   8:{ TYPE:Pad, SIZE:4 }
                   }

    animation_desc = { TYPE:Struct, NAME:"animation", SIZE:180,
                       0:{ TYPE:StrLatin1, NAME:"name", SIZE:32 },
                       1:{ TYPE:Enum16, NAME:"type",
                           0:{ NAME:"base" },
                           1:{ NAME:"overlay" },
                           2:{ NAME:"replacement" },
                           },
                       2:{ TYPE:SInt16, NAME:"frame_count" },
                       3:{ TYPE:SInt16, NAME:"frame_size" },
                       4:{ TYPE:Enum16, NAME:"frame_info_type",
                           0:{ NAME:"none" },
                           1:{ NAME:"dx,dy" },
                           2:{ NAME:"dx,dy,dyaw" },
                           3:{ NAME:"dx,dy,dz,dyaw" }
                           },
                       5:{ TYPE:SInt32,  NAME:"node_list_checksum" },                       
                       6:{ TYPE:SInt16,  NAME:"node_count" },
                       7:{ TYPE:SInt16,  NAME:"loop_frame_index" },
                       
                       8:{ TYPE:Float,   NAME:"weight" },
                       9:{ TYPE:SInt16,  NAME:"key_frame_index" },
                       10:{ TYPE:SInt16, NAME:"second_key_frame_index" },
                       
                       11:{ TYPE:SInt16,  NAME:"next_animation" },
                       12:{ TYPE:Bool16, NAME:"flags",
                            0:{ NAME:"compressed_data" },
                            1:{ NAME:"world_relative" },
                            2:{ NAME:"pal", GUI_NAME:"25Hz(PAL)" },
                            },
                       13:{ TYPE:SInt16,  NAME:"sound" },
                       14:{ TYPE:SInt16,  NAME:"sound_frame_index" },
                       15:{ TYPE:SInt8,   NAME:"left_foot_frame_index" },
                       16:{ TYPE:SInt8,   NAME:"right_foot_frame_index" },
                       17:{ TYPE:SInt16,  NAME:"unknown_1", ENDIAN:'<' },
                       18:{ TYPE:Float,   NAME:"unknown_2", ENDIAN:'<' },
                       
                       19:{ TYPE:RawDataRef, NAME:"frame_info",
                            EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                            CHILD:{TYPE:BytearrayRaw, NAME:"data",
                                   VISIBLE:False, SIZE:".Count"}
                            },
                       20:{ TYPE:BytesRaw, NAME:"unknown_3", SIZE:44 },
                       21:{ TYPE:SInt32,   NAME:"offset_to_compressed_data" },
                       22:{ TYPE:RawDataRef, NAME:"default_data",
                            EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                            CHILD:{TYPE:BytearrayRaw, NAME:"data",
                                   VISIBLE:False, SIZE:".Count"}
                            },
                       23:{ TYPE:RawDataRef, NAME:"frame_data",
                            EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                            CHILD:{TYPE:BytearrayRaw, NAME:"data",
                                   VISIBLE:False, SIZE:".Count"}
                            }
                       }
    
    descriptor = { TYPE:Container, GUI_NAME:"model_animations",
                   0:com( {1:{ DEFAULT:"antr" },
                           5:{ DEFAULT:4} }, Tag_Header),
                   
                   1:{TYPE:Struct, SIZE:128, GUI_NAME:"Data",
                      0:{ TYPE:Reflexive, NAME:"objects",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"objects_array", MAX:4, 
                                   SUB_STRUCT:object_desc, SIZE:".Count"}
                           },
                      1:{ TYPE:Reflexive, NAME:"units",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"units_array", MAX:32, 
                                   SUB_STRUCT:unit_desc, SIZE:".Count" }
                           },
                      2:{ TYPE:Reflexive, NAME:"weapons",
                          INCLUDE:Reflexive_Struct,
                          CHILD:{ TYPE:Array, NAME:"weapons_array", MAX:1, 
                                   SUB_STRUCT:weapons_desc, SIZE:".Count" }
                          },
                      3:{ TYPE:Reflexive, NAME:"vehicles",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"vehicles_array", MAX:1, 
                                   SUB_STRUCT:vehicle_desc, SIZE:".Count" }
                           },
                      4:{ TYPE:Reflexive, NAME:"devices",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"devices_array", MAX:1, 
                                   SUB_STRUCT:device_desc, SIZE:".Count" }
                           },
                      5:{ TYPE:Reflexive, NAME:"unit_damage",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"unit_damage_array", MAX:176, 
                                   SUB_STRUCT:anim_enum_desc, SIZE:".Count" }
                           },
                      6:{ TYPE:Reflexive, NAME:"first_person_weapons",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"fp_animations_array", MAX:1, 
                                   SUB_STRUCT:fp_animation_desc, SIZE:".Count" }
                           },
                      7:{ TYPE:Reflexive, NAME:"sound_references",
                          INCLUDE:Reflexive_Struct,
                          #no idea why they decided to set it to 257 instead of 256....
                          CHILD:{ TYPE:Array, NAME:"sound_references_array", MAX:257, 
                                  SUB_STRUCT:sound_reference_desc, SIZE:".Count" }
                          },
                      
                      8:{ TYPE:Float, NAME:"limp body node radius" },
                      9:{ TYPE:Bool16, NAME:"flags",
                          0:{ NAME:"compress_all_animations" },
                          1:{ NAME:"force_idle_compression" },
                          },
                      10:{ TYPE:Pad, SIZE:2 },
                      
                      11:{ TYPE:Reflexive, NAME:"nodes",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"nodes_array", MAX:64, 
                                   SUB_STRUCT:nodes_desc, SIZE:".Count" }
                           },
                      12:{ TYPE:Reflexive, NAME:"animations",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{ TYPE:Array, NAME:"nodes_array", MAX:256, 
                                   SUB_STRUCT:animation_desc, SIZE:".Count" }
                           }
                      }
                   }
