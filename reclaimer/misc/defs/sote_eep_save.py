from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from supyr_struct.fields import *

def get():
    return SoteEepDef

class SoteEepDef(TagDef):
    
    ext = ".eep"
    
    tag_id = "sote_eep_save"

    endian = ">"
    
    Weapons = { TYPE:Struct,
                0:{ TYPE:UInt8, GUI_NAME:"Pulse"},
                1:{ TYPE:UInt8, GUI_NAME:"Flame"},
                2:{ TYPE:UInt8, GUI_NAME:"Seeker"},
                3:{ TYPE:UInt8, GUI_NAME:"Stunner"},
                4:{ TYPE:UInt8, GUI_NAME:"Disruptor"},
                }

    Save_File = {TYPE:Struct, SIZE:122, GUI_NAME:"Save File",
                 0:{ TYPE:UInt8, GUI_NAME:"File CRC 1",
                     DEFAULT:0, EDITABLE:False },
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
                 4:{ TYPE:StrLatin1, GUI_NAME:"Filename", SIZE:16,
                     DEFAULT:"New Player"},
                 5:{ TYPE:BitStruct, GUI_NAME:"Settings", SIZE:3, ENDIAN:"<",
                     #I only realized this is a big endian file format after I wrote
                     #this section and I don't want to have to edit the offsets
                     0:{ TYPE:BitBool, GUI_NAME:"Flags", SIZE:12,
                         0:{ GUI_NAME:"File Exists", VALUE:0x1 },
                         1:{ GUI_NAME:"Overlay Displays Off", VALUE:0x10 },
                         2:{ GUI_NAME:"Seeker Camera Off", VALUE:0x100 },
                        },
                     1:{TYPE:BitEnum, GUI_NAME:"SFX Volume", SIZE:2,
                        0:{GUI_NAME:"Loud"},
                        1:{GUI_NAME:"Medium"},
                        2:{GUI_NAME:"Soft"},
                        3:{GUI_NAME:"Off"} },
                     2:{ TYPE:Pad, SIZE:2 },
                     3:{TYPE:BitEnum, GUI_NAME:"Music Volume", SIZE:2,
                        0:{GUI_NAME:"Loud"},
                        1:{GUI_NAME:"Medium"},
                        2:{GUI_NAME:"Soft"},
                        3:{GUI_NAME:"Off"} },
                     4:{ TYPE:Pad, SIZE:2 },
                     5:{TYPE:BitEnum, GUI_NAME:"Sound Panning", SIZE:1,
                        0:{GUI_NAME:"Stereo"},
                        1:{GUI_NAME:"Mono"} }
                     },
                 
                 6:{ TYPE:Enum24, GUI_NAME:"Control Scheme",
                     0:{GUI_NAME:"Standard",               VALUE:0x00000},
                     1:{GUI_NAME:"Standard(View Lock)",    VALUE:0x10001},
                     2:{GUI_NAME:"Traditional",            VALUE:0x20002},
                     3:{GUI_NAME:"Traditional(View Lock)", VALUE:0x30003},
                     4:{GUI_NAME:"Alternate",              VALUE:0x40004},
                     5:{GUI_NAME:"Alternate(View Lock)",   VALUE:0x50005},
                     6:{GUI_NAME:"Strafe",                 VALUE:0x60006},
                     7:{GUI_NAME:"Strafe(View Lock)",      VALUE:0x70007}
                     },
                 7:{ TYPE:Enum24, GUI_NAME:"Button Mapping",
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
                     0:combine( {GUI_NAME:"Battle of Hoth"}, Weapons),
                     1:combine( {GUI_NAME:"Escape from Echo Base"}, Weapons),
                     2:combine( {GUI_NAME:"The Asteroid Field"}, Weapons),
                     3:combine( {GUI_NAME:"Ord Mantell Junkyard"}, Weapons),
                     4:combine( {GUI_NAME:"Gall Spaceport"}, Weapons),
                     5:combine( {GUI_NAME:"Mos Eisley and Beggars Canyon"}, Weapons),
                     6:combine( {GUI_NAME:"Imperial Freighter Suprosa"}, Weapons),
                     7:combine( {GUI_NAME:"Sewers of the Imperial City"}, Weapons),
                     8:combine( {GUI_NAME:"Xizors Palace"}, Weapons),
                     9:combine( {GUI_NAME:"Skyhook Battle"}, Weapons),
                     },
                 10:{ TYPE:Pad, SIZE:1 },
                 11:{ TYPE:Struct, SIZE:20, GUI_NAME:"Completion Times",
                      #measured in seconds
                      0:{ TYPE:UInt16, GUI_NAME:"Battle of Hoth" },
                      1:{ TYPE:UInt16, GUI_NAME:"Escape from Echo Base" },
                      2:{ TYPE:UInt16, GUI_NAME:"The Asteroid Field" },
                      3:{ TYPE:UInt16, GUI_NAME:"Ord Mantell Junkyard" },
                      4:{ TYPE:UInt16, GUI_NAME:"Gall Spaceport" },
                      5:{ TYPE:UInt16, GUI_NAME:"Mos Eisley and Beggars Canyon" },
                      6:{ TYPE:UInt16, GUI_NAME:"Imperial Freighter Suprosa" },
                      7:{ TYPE:UInt16, GUI_NAME:"Sewers of the Imperial City" },
                      8:{ TYPE:UInt16, GUI_NAME:"Xizors Palace" },
                      9:{ TYPE:UInt16, GUI_NAME:"Skyhook Battle" }
                      },
                 12:{ TYPE:Struct, SIZE:10, GUI_NAME:"Challenge Points",
                      0:{ GUI_NAME:"Battle of Hoth",
                          TYPE:UInt8, MIN:0, MAX:3 },
                      1:{ GUI_NAME:"Escape from Echo Base",
                          TYPE:UInt8, MIN:0, MAX:10 },
                      2:{ GUI_NAME:"The Asteroid Field",
                          TYPE:UInt8, MIN:0, MAX:6 },
                      3:{ GUI_NAME:"Ord Mantell Junkyard",
                          TYPE:UInt8, MIN:0, MAX:12 },
                      4:{ GUI_NAME:"Gall Spaceport",
                          TYPE:UInt8, MIN:0, MAX:15 },
                      5:{ GUI_NAME:"Mos Eisley and Beggars Canyon",
                          TYPE:UInt8, MIN:0, MAX:12 },
                      6:{ GUI_NAME:"Imperial Freighter Suprosa",
                          TYPE:UInt8, MIN:0, MAX:10 },
                      7:{ GUI_NAME:"Sewers of the Imperial City",
                          TYPE:UInt8, MIN:0, MAX:9 },
                      8:{ GUI_NAME:"Xizors Palace",
                          TYPE:UInt8, MIN:0, MAX:10 },
                      9:{ GUI_NAME:"Skyhook Battle",
                          TYPE:UInt8, MIN:0, MAX:0 }
                      },
                 #OR-ing this value with the first checksum byte must produce 255, b'\xff'.
                 #If it doesnt then the save is considered corrupt and is erased.
                 #The first checksum byte will be defaulted to 0, and this one to 255.
                 13:{ TYPE:UInt8, GUI_NAME:"File CRC 2", DEFAULT:255, EDITABLE:False },
                 14:{ TYPE:Pad, SIZE:1 }
                 }
    
    descriptor = { TYPE:Container, GUI_NAME:"SotE EEP Save File",
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
                        SUB_STRUCT:Save_File
                        },
                     2:{ TYPE:Struct, GUI_NAME:"Footer",
                         #if this is not b'\x53\x68\x26' then the file wont load
                         0:{ TYPE:UInt24, GUI_NAME:"Magic Constant 2",
                             EDITABLE:False, DEFAULT:b'\x53\x68\x26' },
                         
                         #OR-ing this value with the first checksum byte must produce 255, b'\xff'.
                         #If it doesnt then the save is considered corrupt and is erased.
                         #The first checksum byte will be defaulted to 0, and this one to 255.
                         1:{ TYPE:UInt8, GUI_NAME:"EEP CRC 2", DEFAULT:255, EDITABLE:False },
                         2:{ TYPE:Pad, SIZE:14 }
                         }
                     }