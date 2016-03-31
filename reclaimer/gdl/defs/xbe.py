from supyr_struct.defs.executables.xbe import *

def get():
    return GdlXbeDef

class GdlXbeDef(XbeDef):

    make_gui_names = True

    special_types = { TYPE:Bool32, NAME:"Flags",
                      0:{NAME:"Levitate", VALUE:1},
                      1:{NAME:"X_Ray", VALUE:2},
                      2:{NAME:"Invisible", VALUE:4},
                      3:{NAME:"Stop_Time", VALUE:8},
                      4:{NAME:"Fire_Breath", VALUE:16},
                      5:{NAME:"Acid_Breath", VALUE:32},
                      6:{NAME:"Elec_Breath", VALUE:64},
                      7:{NAME:"Phoenix", VALUE:128},
                      8:{NAME:"Growth", VALUE:256},
                      9:{NAME:"Shrink", VALUE:512},
                      10:{NAME:"Pojo", VALUE:1024},
                      11:{NAME:"Skorn_Horns", VALUE:4096},
                      12:{NAME:"Skorn_Mask", VALUE:8192},
                      13:{NAME:"Skorn_Gauntlet_R", VALUE:16384},
                      14:{NAME:"Skorn_Gauntlet_L", VALUE:32768},
                      15:{NAME:"Hand_of_Death", VALUE:2097152},
                      16:{NAME:"Health_Vampire", VALUE:4194304},
                      17:{NAME:"Dummy", VALUE:262144},
                      18:{NAME:"Mikey", VALUE:1048576},
                      19:{NAME:"Health", VALUE:131072},
                      20:{NAME:"Speed", VALUE:65536},
                      21:{NAME:"Turbo", VALUE:524288}
                   }
    
    armor_types = { TYPE:Bool32, NAME:"Flags",
                    0:{NAME:"Resist_Fire", VALUE:1},
                    1:{NAME:"Resist_Elec", VALUE:2},
                    2:{NAME:"Resist_Light", VALUE:4},
                    3:{NAME:"Resist_Acid", VALUE:8},
                    4:{NAME:"Resist_Magic", VALUE:16},
                
                    5:{NAME:"Immune_Fire", VALUE:256},
                    6:{NAME:"Immune_Elec", VALUE:512},
                    7:{NAME:"Immune_Light", VALUE:1024},
                    8:{NAME:"Immune_Acid", VALUE:2048},
                    9:{NAME:"Immune_Magic", VALUE:4096},
                    10:{NAME:"Immune_Gas", VALUE:8192},
                    11:{NAME:"Immune_Knockback", VALUE:262144},
                
                    12:{NAME:"Invulnerability_Silver", VALUE:65536},
                    13:{NAME:"Invulnerability_Gold", VALUE:1048576},
                
                    14:{NAME:"Armor_Reflect", VALUE:131072},
                    15:{NAME:"Armor_Reflect2", VALUE:16777216},
                    16:{NAME:"Armor_Protect", VALUE:8388608},
                    17:{NAME:"Armor_Fire", VALUE:2097152},
                    18:{NAME:"Armor_Elec", VALUE:4194304},
                
                    19:{NAME:"Antideath", VALUE:524288}
                    }
    
    #these are for when the program can handle displaying
    #structs and the library can handle union fields
    weapon_types = { TYPE:BitStruct, SIZE:4, NAME:"Flags",
                     0:{TYPE:BitUEnum, NAME:"Weapon_Type", SIZE:4,
                        0:{NAME:"Normal"},
                        1:{NAME:"Fire"},
                        2:{NAME:"Elec"},
                        3:{NAME:"Light"},
                        4:{NAME:"Acid"},
                        },
                     1:{TYPE:BitBool, NAME:"Weapon_Flags", SIZE:28,
                        0:{NAME:"Knockback", VALUE:16},
                        1:{NAME:"Knockdown", VALUE:32},
                        2:{NAME:"Whirlwind", VALUE:65536},
                        3:{NAME:"Three_Way", VALUE:524288},
                        4:{NAME:"Five_Way", VALUE:4194304},
                        5:{NAME:"Super", VALUE:1048576},
                        6:{NAME:"Heals", VALUE:8388608},
                        7:{NAME:"Turbo", VALUE:33554432},
                        8:{NAME:"Hammer", VALUE:268435456},
                        9:{NAME:"Rapid", VALUE:536870912},
                        10:{NAME:"Reflect", VALUE:2097152}
                        }
                     }
    
    weapon_types = { TYPE:Bool32, NAME:"Flags",
                     0:{NAME:"Knockback", VALUE:16},
                     1:{NAME:"Knockdown", VALUE:32},
                     2:{NAME:"Whirlwind", VALUE:65536},
                     3:{NAME:"Three_Way", VALUE:524288},
                     4:{NAME:"Five_Way", VALUE:4194304},
                     5:{NAME:"Super", VALUE:1048576},
                     6:{NAME:"Heals", VALUE:8388608},
                     7:{NAME:"Turbo", VALUE:33554432},
                     8:{NAME:"Hammer", VALUE:268435456},
                     9:{NAME:"Rapid", VALUE:536870912},
                     10:{NAME:"Fireball", VALUE:262144},
                     11:{NAME:"Reflect", VALUE:2097152}
                     }



    descriptor = { TYPE:Container, NAME:"Gauntlet_Dark_Legacy_XBE",
                   0:XbeDef.xbe_image_header,
                   1:XbeDef.xbe_certificate,
                   2:XbeDef.xbe_sec_headers,
                   3:XbeDef.xbe_lib_ver_headers,
                   4:{TYPE:Array, NAME:"Secret_Characters", SIZE:27, POINTER:1135088,
                      SUB_STRUCT:{TYPE:Struct, SIZE:36, NAME:"Character",                         
                                  0:{ TYPE:Enum32, NAME:"Color",
                                      0:{NAME:"Yellow"},
                                      1:{NAME:"Blue"},
                                      2:{NAME:"Red"},
                                      3:{NAME:"Green"}
                                      },
                                  
                                  1:{ TYPE:Enum32, NAME:"Type",
                                      0:{NAME:"Warrior"},
                                      1:{NAME:"Valkyrie"},
                                      2:{NAME:"Wizard"},
                                      3:{NAME:"Archer"},
                                      4:{NAME:"Dwarf"},
                                      5:{NAME:"Knight"},
                                      6:{NAME:"Sorceress"},
                                      7:{NAME:"Jester"},
                                   
                                      8:{NAME:"Minotaur"},
                                      9:{NAME:"Falconess"},
                                      10:{NAME:"Jackal"},
                                      11:{NAME:"Tigress"},
                                      12:{NAME:"Ogre"},
                                      13:{NAME:"Unicorn"},
                                      14:{NAME:"Medusa"},
                                      15:{NAME:"Hyena"},
                                      },
                                  2:{ TYPE:StrLatin1,  NAME:"Code", SIZE:7 },
                                  3:{ TYPE:Pad, SIZE:1 },
                                  4:{ TYPE:StrLatin1,  NAME:"Directory", SIZE:16 },
                                  5:{ TYPE:Bool32,     NAME:"Flags",
                                      0:{NAME:"Disable", VALUE:1 }
                                      }
                                  }
                      },
                   
                   5:{TYPE:Array, NAME:"Cheats", SIZE:18, POINTER:1136064,
                      SUB_STRUCT:{TYPE:Struct, NAME:"Cheat",
                                  0:{ TYPE:StrLatin1, SIZE:7,
                                      OFFSET:0, NAME:"Code"},
                                  1:{ TYPE:Pad, SIZE:1 },
                                  2:{ TYPE:Enum32, NAME:"Type",
                                      0:{NAME:"Gold",   VALUE:1},
                                      1:{NAME:"Key",    VALUE:2},
                                      2:{NAME:"Potion", VALUE:4},

                                      #these 3 utilize the below flags
                                      3:{NAME:"Weapon",  VALUE:5},
                                      4:{NAME:"Armor",   VALUE:6},
                                      5:{NAME:"Special", VALUE:9}
                                      },
                                  3:{ TYPE:Float,  NAME:"Add" },
                                  4:{ TYPE:Bool32, NAME:"Flags" }
                                  }
                       }
                   }

    subdefs = { 'weapon_types':weapon_types,
                'special_types':special_types,
                'armor_types':armor_types,
                'no_types':{ TYPE:Bool32, NAME:"Flags" }}
