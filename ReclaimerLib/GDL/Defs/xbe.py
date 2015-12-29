from supyr_struct.Defs.executables.xbe import *

def Construct():
    return GDL_XBE_Definition

class GDL_XBE_Definition(XBE_Def):

    Special_Types = { TYPE:Bool32, GUI_NAME:"Flags",
                      0:{GUI_NAME:"Levitate", VALUE:1},
                      1:{GUI_NAME:"X Ray", VALUE:2},
                      2:{GUI_NAME:"Invisible", VALUE:4},
                      3:{GUI_NAME:"Stop Time", VALUE:8},
                      4:{GUI_NAME:"Fire Breath", VALUE:16},
                      5:{GUI_NAME:"Acid Breath", VALUE:32},
                      6:{GUI_NAME:"Elec Breath", VALUE:64},
                      7:{GUI_NAME:"Phoenix", VALUE:128},
                      8:{GUI_NAME:"Growth", VALUE:256},
                      9:{GUI_NAME:"Shrink", VALUE:512},
                      10:{GUI_NAME:"Pojo", VALUE:1024},
                      11:{GUI_NAME:"Skorn Horns", VALUE:4096},
                      12:{GUI_NAME:"Skorn Mask", VALUE:8192},
                      13:{GUI_NAME:"Skorn R Gauntlet", VALUE:16384},
                      14:{GUI_NAME:"Skorn L Gauntlet", VALUE:32768},
                      15:{GUI_NAME:"Speed", VALUE:65536},
                      16:{GUI_NAME:"Health", VALUE:131072},
                      17:{GUI_NAME:"Dummy", VALUE:262144},
                      18:{GUI_NAME:"Turbo", VALUE:524288},
                      19:{GUI_NAME:"Mikey", VALUE:1048576},
                      20:{GUI_NAME:"Hand of Death", VALUE:2097152},
                      21:{GUI_NAME:"Health Vampire", VALUE:4194304}
                   }
    
    Armor_Types = { TYPE:Bool32, GUI_NAME:"Flags",
                    0:{GUI_NAME:"Resist Fire", VALUE:1},
                    1:{GUI_NAME:"Resist Elec", VALUE:2},
                    2:{GUI_NAME:"Resist Light", VALUE:4},
                    3:{GUI_NAME:"Resist Acid", VALUE:8},
                    4:{GUI_NAME:"Resist Magic", VALUE:16},
                
                    5:{GUI_NAME:"Immune Fire", VALUE:256},
                    6:{GUI_NAME:"Immune Elec", VALUE:512},
                    7:{GUI_NAME:"Immune Light", VALUE:1024},
                    8:{GUI_NAME:"Immune Acid", VALUE:2048},
                    9:{GUI_NAME:"Immune Magic", VALUE:4096},
                    10:{GUI_NAME:"Immune Gas", VALUE:8192},
                    11:{GUI_NAME:"Immune Knockback", VALUE:262144},
                
                    12:{GUI_NAME:"Silver Invuln", VALUE:65536},
                    13:{GUI_NAME:"Gold Invuln", VALUE:1048576},
                
                    14:{GUI_NAME:"Antideath", VALUE:524288},
                
                    15:{GUI_NAME:"Armor Reflect", VALUE:131072},
                    16:{GUI_NAME:"Armor Fire", VALUE:2097152},
                    17:{GUI_NAME:"Armor Elec", VALUE:4194304},
                    18:{GUI_NAME:"Armor Protect", VALUE:8388608},
                    19:{GUI_NAME:"Armor Reflect2", VALUE:16777216}
                    }
    '''
    #these are for when the library can handle displaying structs
    Weapon_Types = { TYPE:Bit_Struct, SIZE:4, GUI_NAME:"Flags",
                     0:{TYPE:Bit_Enum, GUI_NAME:"Weapon Type", SIZE:4,
                        0:{GUI_NAME:"Normal"},
                        1:{GUI_NAME:"Fire"},
                        2:{GUI_NAME:"Elec"},
                        3:{GUI_NAME:"Light"},
                        4:{GUI_NAME:"Acid"},
                        },
                     1:{TYPE:Bit_Bool, GUI_NAME:"Weapon Flags", SIZE:28,
                        0:{GUI_NAME:"Knockback", VALUE:16},
                        1:{GUI_NAME:"Knockdown", VALUE:32},
                        2:{GUI_NAME:"Whirlwind", VALUE:65536},
                        3:{GUI_NAME:"Three Way", VALUE:524288},
                        4:{GUI_NAME:"Five Way", VALUE:4194304},
                        5:{GUI_NAME:"Super", VALUE:1048576},
                        6:{GUI_NAME:"Heals", VALUE:8388608},
                        7:{GUI_NAME:"Turbo", VALUE:33554432},
                        8:{GUI_NAME:"Hammer", VALUE:268435456},
                        9:{GUI_NAME:"Rapid", VALUE:536870912},
                        10:{GUI_NAME:"Reflect", VALUE:2097152}
                        }
                     }
    '''
    
    Weapon_Types = { TYPE:Bool32, GUI_NAME:"Flags",
                     0:{GUI_NAME:"Knockback", VALUE:16},
                     1:{GUI_NAME:"Knockdown", VALUE:32},
                     2:{GUI_NAME:"Whirlwind", VALUE:65536},
                     3:{GUI_NAME:"Three Way", VALUE:524288},
                     4:{GUI_NAME:"Five Way", VALUE:4194304},
                     5:{GUI_NAME:"Super", VALUE:1048576},
                     6:{GUI_NAME:"Heals", VALUE:8388608},
                     7:{GUI_NAME:"Turbo", VALUE:33554432},
                     8:{GUI_NAME:"Hammer", VALUE:268435456},
                     9:{GUI_NAME:"Rapid", VALUE:536870912},
                     10:{GUI_NAME:"Fireball", VALUE:262144},
                     11:{GUI_NAME:"Reflect", VALUE:2097152}
                     }



    Tag_Structure = {TYPE:Container, GUI_NAME:"Gauntlet Dark Legacy XBE",
                     0:XBE_Def.XBE_Image_Header,
                     1:XBE_Def.XBE_Certificate,
                     2:XBE_Def.XBE_Sec_Headers,
                     3:XBE_Def.XBE_Lib_Ver_Headers,
                     4:{TYPE:Array, GUI_NAME:"Secret Characters", SIZE:27, POINTER:1135088,
                        SUB_STRUCT:{TYPE:Struct, SIZE:36, GUI_NAME:"Secret Character",                         
                                    0:{ TYPE:Enum32, OFFSET:0, GUI_NAME:"Color",
                                        0:{GUI_NAME:"Yellow"},
                                        1:{GUI_NAME:"Blue"},
                                        2:{GUI_NAME:"Red"},
                                        3:{GUI_NAME:"Green"}
                                        },
                                    
                                    1:{ TYPE:Enum32, OFFSET:4, GUI_NAME:"Character Type",
                                        0:{GUI_NAME:"Warrior"},
                                        1:{GUI_NAME:"Valkyrie"},
                                        2:{GUI_NAME:"Wizard"},
                                        3:{GUI_NAME:"Archer"},
                                        4:{GUI_NAME:"Dwarf"},
                                        5:{GUI_NAME:"Knight"},
                                        6:{GUI_NAME:"Sorceress"},
                                        7:{GUI_NAME:"Jester"},
                                     
                                        8:{GUI_NAME:"Minotaur"},
                                        9:{GUI_NAME:"Falconess"},
                                        10:{GUI_NAME:"Jackal"},
                                        11:{GUI_NAME:"Tigress"},
                                        12:{GUI_NAME:"Ogre"},
                                        13:{GUI_NAME:"Unicorn"},
                                        14:{GUI_NAME:"Medusa"},
                                        15:{GUI_NAME:"Hyena"},
                                        },
                                    2:{ TYPE:Str_Latin1, OFFSET:8, GUI_NAME:"Activation Code", SIZE:7},
                                    3:{ TYPE:Str_Latin1, OFFSET:16, GUI_NAME:"Directory", SIZE:16 },
                                    4:{ TYPE:Bool32,     OFFSET:32, GUI_NAME:"Flags",
                                        0:{NAME:"Disable", VALUE:1}
                                        }
                                    }
                        },
                     
                     5:{TYPE:Array, NAME:"Cheats", SIZE:18, POINTER:1136064,
                        SUB_STRUCT:{TYPE:Struct, GUI_NAME:"Cheat", CHILD_ROOT:True,
                                    0:{ TYPE:Str_Latin1, SIZE:7,
                                        OFFSET:0, GUI_NAME:"Activation Code"},
                                    1:{ TYPE:Enum32, OFFSET:8, GUI_NAME:"Item Type",
                                        0:{GUI_NAME:"Gold", VALUE:1},
                                        1:{GUI_NAME:"Key", VALUE:2},
                                        2:{GUI_NAME:"Potion", VALUE:4},

                                        #these 3 utilize the below flags
                                        3:{GUI_NAME:"Weapon",  VALUE:5},
                                        4:{GUI_NAME:"Armor",   VALUE:6},
                                        5:{GUI_NAME:"Special", VALUE:9}
                                        },
                                    2:{ TYPE:Float,  OFFSET:12, NAME:"Add" },
                                    3:{ TYPE:Bool32, OFFSET:16, NAME:"Flags" }
                                    }
                         }
                     }

    Structures = {'Weapon_Types':Weapon_Types,
                  'Special_Types':Special_Types,
                  'Armor_Types':Armor_Types,
                  'No_Types':{ TYPE:Bool32, NAME:"Flags" }}
