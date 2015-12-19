from supyr_struct.Defs.Tag_Def import Tag_Def
from supyr_struct.Defs.Common_Structures import *
from supyr_struct.Field_Types import *

def Construct():
    return SotE_EEP_Definition

class SotE_EEP_Definition(Tag_Def):
    
    Ext = ".eep"
    
    Cls_ID = "sote_eep_save"

    Endian = ">"
    
    Weapons = { TYPE:Struct,
                0:{ TYPE:UInt8, GUI_NAME:"Pulse"},
                1:{ TYPE:UInt8, GUI_NAME:"Flame"},
                2:{ TYPE:UInt8, GUI_NAME:"Seeker"},
                3:{ TYPE:UInt8, GUI_NAME:"Stunner"},
                4:{ TYPE:UInt8, GUI_NAME:"Disruptor"},
                }
    
    Tag_Structure = {TYPE:Container, GUI_NAME:"SotE EEP Save File",
                     0:{TYPE:Struct, NAME:"Header",
                        0:{ TYPE:UInt8,  GUI_NAME:"EEP CRC 1", EDITABLE:False},
                        #if this is not b'\xFF\x53\x68\x26' then the file wont load
                        1:{ TYPE:UInt32, GUI_NAME:"Magic Constant 1",
                            EDITABLE:False, DEFAULT:b'\xFF\x53\x68\x26'},
                        2:{ TYPE:Enum8,  GUI_NAME:"File just beaten",
                            0:{NAME:"No File"},
                            1:{NAME:"File 1"},
                            2:{NAME:"File 2"},
                            3:{NAME:"File 3"},
                            4:{NAME:"File 4"}
                            }
                        },
                     1:{TYPE:Array, GUI_NAME:"Save Files", SIZE:4, MIN:4, MAX:4,
                        SUB_STRUCT:{TYPE:Struct, SIZE:122, GUI_NAME:"Save File",
                                       0:{ TYPE:UInt8, GUI_NAME:"File CRC 1", DEFAULT:0, EDITABLE:False },
                                       1:{ TYPE:Enum8, GUI_NAME:"Difficulty",
                                           0:{GUI_NAME:"None"},
                                           1:{GUI_NAME:"Easy"},
                                           2:{GUI_NAME:"Medium"},
                                           3:{GUI_NAME:"Hard"},
                                           4:{GUI_NAME:"Jedi"}
                                           },
                                       2:{ TYPE:Enum8, GUI_NAME:"Current Level",
                                           0:{ GUI_NAME:"Battle of Hoth"},
                                           1:{ GUI_NAME:"Escape from Echo Base"},
                                           2:{ GUI_NAME:"The Asteroid Field"},
                                           3:{ GUI_NAME:"Ord Mantell Junkyard"},
                                           4:{ GUI_NAME:"Gall Spaceport"},
                                           5:{ GUI_NAME:"Mos Eisley and Beggars Canyon"},
                                           6:{ GUI_NAME:"Imperial Freighter Suprosa"},
                                           7:{ GUI_NAME:"Sewers of the Imperial City"},
                                           8:{ GUI_NAME:"Xizors Palace"},
                                           9:{ GUI_NAME:"Skyhook Battle"}
                                           },
                                       3:{ TYPE:Bool8, GUI_NAME:"Flags",
                                           0:{ GUI_NAME:"Game Beaten", VALUE:1 },
                                           1:{ GUI_NAME:"Game Started", VALUE:16 }
                                           },
                                       4:{ TYPE:Str_Latin1, GUI_NAME:"Filename", SIZE:16,
                                           DEFAULT:"New Player"},
                                       5:{ TYPE:Bit_Struct, GUI_NAME:"Settings", SIZE:3, ENDIAN:"<",
                                           #I only realized this is a big endian file format after I wrote
                                           #this section and I don't want to have to edit the offsets
                                           0:{ TYPE:Bit_Bool, GUI_NAME:"Flags", SIZE:12,
                                               0:{ GUI_NAME:"File Exists", VALUE:0x1 },
                                               1:{ GUI_NAME:"Overlay Displays Off", VALUE:0x10 },
                                               2:{ GUI_NAME:"Seeker Camera Off", VALUE:0x100 },
                                              },
                                           1:{TYPE:Bit_Enum, GUI_NAME:"SFX Volume", SIZE:2,
                                              0:{GUI_NAME:"Loud"},
                                              1:{GUI_NAME:"Medium"},
                                              2:{GUI_NAME:"Soft"},
                                              3:{GUI_NAME:"Off"} },
                                           2:{ PAD:2 },
                                           3:{TYPE:Bit_Enum, GUI_NAME:"Music Volume", SIZE:2,
                                              0:{GUI_NAME:"Loud"},
                                              1:{GUI_NAME:"Medium"},
                                              2:{GUI_NAME:"Soft"},
                                              3:{GUI_NAME:"Off"} },
                                           4:{ PAD:2 },
                                           5:{TYPE:Bit_Enum, GUI_NAME:"Sound Panning", SIZE:1,
                                              0:{GUI_NAME:"Stereo"},
                                              1:{GUI_NAME:"Mono"} }
                                           },
                                       
                                       6:{ TYPE:Big_Enum, GUI_NAME:"Control Scheme", SIZE:3,
                                           0:{GUI_NAME:"Standard", VALUE:0},
                                           1:{GUI_NAME:"Standard(View Lock)", VALUE:0x10001},
                                           2:{GUI_NAME:"Traditional", VALUE:0x020002},
                                           3:{GUI_NAME:"Traditional(View Lock)", VALUE:0x030003},
                                           4:{GUI_NAME:"Alternate", VALUE:0x040004},
                                           5:{GUI_NAME:"Alternate(View Lock)", VALUE:0x050005},
                                           6:{GUI_NAME:"Strafe", VALUE:0x060006},
                                           7:{GUI_NAME:"Strafe(View Lock)", VALUE:0x070007}
                                           },
                                       7:{ TYPE:Big_Enum, GUI_NAME:"Button Mapping", SIZE:3,
                                           0:{GUI_NAME:"Standard", VALUE:0x000000},
                                           1:{GUI_NAME:"Alternate", VALUE:0x020202}
                                           },
                                       8:{ TYPE:Struct, SIZE:10, GUI_NAME:"Extra Lives",
                                           0:{ TYPE:UInt8, GUI_NAME:"Battle of Hoth", DEFAULT:3},
                                           1:{ TYPE:UInt8, GUI_NAME:"Escape from Echo Base", DEFAULT:3},
                                           2:{ TYPE:UInt8, GUI_NAME:"The Asteroid Field", DEFAULT:3},
                                           3:{ TYPE:UInt8, GUI_NAME:"Ord Mantell Junkyard", DEFAULT:3},
                                           4:{ TYPE:UInt8, GUI_NAME:"Gall Spaceport", DEFAULT:3},
                                           5:{ TYPE:UInt8, GUI_NAME:"Mos Eisley and Beggars Canyon", DEFAULT:3},
                                           6:{ TYPE:UInt8, GUI_NAME:"Imperial Freighter Suprosa", DEFAULT:3},
                                           7:{ TYPE:UInt8, GUI_NAME:"Sewers of the Imperial City", DEFAULT:3},
                                           8:{ TYPE:UInt8, GUI_NAME:"Xizors Palace", DEFAULT:3},
                                           9:{ TYPE:UInt8, GUI_NAME:"Skyhook Battle", DEFAULT:3}
                                           },
                                       9:{ TYPE:Struct, GUI_NAME:"Ammo Counts", SIZE:50,
                                           0:Combine( {GUI_NAME:"Battle of Hoth"}, Weapons),
                                           1:Combine( {GUI_NAME:"Escape from Echo Base"}, Weapons),
                                           2:Combine( {GUI_NAME:"The Asteroid Field"}, Weapons),
                                           3:Combine( {GUI_NAME:"Ord Mantell Junkyard"}, Weapons),
                                           4:Combine( {GUI_NAME:"Gall Spaceport"}, Weapons),
                                           5:Combine( {GUI_NAME:"Mos Eisley and Beggars Canyon"}, Weapons),
                                           6:Combine( {GUI_NAME:"Imperial Freighter Suprosa"}, Weapons),
                                           7:Combine( {GUI_NAME:"Sewers of the Imperial City"}, Weapons),
                                           8:Combine( {GUI_NAME:"Xizors Palace"}, Weapons),
                                           9:Combine( {GUI_NAME:"Skyhook Battle"}, Weapons),
                                           },
                                       10:{ PAD:1 },
                                       11:{ TYPE:Struct, SIZE:20, GUI_NAME:"Completion Times",
                                           #measured in seconds
                                           0:{ TYPE:UInt16, GUI_NAME:"Battle of Hoth"},
                                           1:{ TYPE:UInt16, GUI_NAME:"Escape from Echo Base"},
                                           2:{ TYPE:UInt16, GUI_NAME:"The Asteroid Field"},
                                           3:{ TYPE:UInt16, GUI_NAME:"Ord Mantell Junkyard"},
                                           4:{ TYPE:UInt16, GUI_NAME:"Gall Spaceport"},
                                           5:{ TYPE:UInt16, GUI_NAME:"Mos Eisley and Beggars Canyon"},
                                           6:{ TYPE:UInt16, GUI_NAME:"Imperial Freighter Suprosa"},
                                           7:{ TYPE:UInt16, GUI_NAME:"Sewers of the Imperial City"},
                                           8:{ TYPE:UInt16, GUI_NAME:"Xizors Palace"},
                                           9:{ TYPE:UInt16, GUI_NAME:"Skyhook Battle"}
                                           },
                                       12:{ TYPE:Struct, SIZE:10, GUI_NAME:"Challenge Points",
                                            0:{ GUI_NAME:"Battle of Hoth",
                                                TYPE:UInt8, MIN:0, MAX:3},
                                            1:{ GUI_NAME:"Escape from Echo Base",
                                                TYPE:UInt8, MIN:0, MAX:10},
                                            2:{ GUI_NAME:"The Asteroid Field",
                                                TYPE:UInt8, MIN:0, MAX:6},
                                            3:{ GUI_NAME:"Ord Mantell Junkyard",
                                                TYPE:UInt8, MIN:0, MAX:12},
                                            4:{ GUI_NAME:"Gall Spaceport",
                                                TYPE:UInt8, MIN:0, MAX:15},
                                            5:{ GUI_NAME:"Mos Eisley and Beggars Canyon",
                                                TYPE:UInt8, MIN:0, MAX:12},
                                            6:{ GUI_NAME:"Imperial Freighter Suprosa",
                                                TYPE:UInt8, MIN:0, MAX:10},
                                            7:{ GUI_NAME:"Sewers of the Imperial City",
                                                TYPE:UInt8, MIN:0, MAX:9},
                                            8:{ GUI_NAME:"Xizors Palace",
                                                TYPE:UInt8, MIN:0, MAX:10},
                                            9:{ GUI_NAME:"Skyhook Battle",
                                                TYPE:UInt8, MIN:0, MAX:0}
                                           },
                                       #Adding this value to the first checksum byte must equate to 255.
                                       #If it doesnt then the save is considered corrupt and is erased.
                                       #The first checksum byte will be defaulted to 0, and this one to 255.
                                       13:{ TYPE:UInt8, GUI_NAME:"File CRC 2", DEFAULT:255, EDITABLE:False},
                                       14:{ PAD:1 }
                                       }
                        },
                     2:{TYPE:Struct, GUI_NAME:"Footer",
                        #if this is not b'\x53\x68\x26' then the file wont load
                        0:{ TYPE:Big_UInt, GUI_NAME:"Magic Constant 2",
                            EDITABLE:False, SIZE:3, DEFAULT:b'\x53\x68\x26'},
                        
                        #Adding this value to the first checksum byte must equate to 255.
                        #If it doesnt then the save is considered corrupt and is erased.
                        #The first checksum byte will be defaulted to 0, and this one to 255.
                        1:{ TYPE:UInt8, GUI_NAME:"EEP CRC 2", DEFAULT:255, EDITABLE:False},
                        2:{ PAD:14 }
                        }
                     }
