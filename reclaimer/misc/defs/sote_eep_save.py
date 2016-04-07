from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from supyr_struct.fields import *

HEADER_MAGIC_1 = b'\xFF\x53\x68\x26'
HEADER_MAGIC_2 = HEADER_MAGIC_1[1:]

def get(): return sote_rep_def
    
weapons = Struct( "weapons",
    UInt8("Pulse"),
    UInt8("Flame"),
    UInt8("Seeker"),
    UInt8("Stunner"),
    UInt8("Disruptor")
    )

save_file = Struct("save file",
    UInt8("file checksum 1", DEFAULT=0, EDITABLE=False),
    UEnum8("difficulty",
        "none",
        "easy",
        "medium",
        "hard",
        "jedi"
        ),
    UEnum8("current level",
        "Battle of Hoth",
        "Escape from Echo Base",
        "The Asteroid Field",
        "Ord Mantell Junkyard",
        "Gall Spaceport",
        "Mos Eisley and Beggars Canyon",
        "Imperial Freighter Suprosa",
        "Sewers of the Imperial City",
        "Xizors Palace",
        "Skyhook Battle"
        ),
    Bool8("flags",
        ("game beaten",  0x1),
        ("game started", 0xF)
        ),
    StrLatin1("filename", SIZE=16, DEFAULT="New Player"),
    BBitStruct("settings",
        #byte 3
        BitUEnum("music volume",
            "loud",
            "medium",
            "soft",
            "off",
            SIZE=2 ),
        Pad(2),
        BitUEnum("sound panning",
            "stereo",
            "mono",
            SIZE=1 ),
        Pad(3),
        #byte 2
        Bit("seeker camera off"),
        Pad(3),
        BitUEnum("sfx volume", 
            "loud",
            "medium",
            "soft",
            "off",
            SIZE=2 ),
        Pad(2),
        #byte 1
        Bit("file exists"),
        Pad(3),
        Bit("overlay displays off")
        ),
    BUEnum24("control scheme",
        ("standard",               0x00000),
        ("standard(view lock)",    0x10001),
        ("traditional",            0x20002),
        ("traditional(view lock)", 0x30003),
        ("alternate",              0x40004),
        ("alternate(view lock)",   0x50005),
        ("strafe",                 0x60006),
        ("strafe(view lock)",      0x70007)
        ),
    BUEnum24("button mapping",
        ("standard",  0x000000),
        ("alternate", 0x020202)
        ),
    Struct("extra lives",
        UInt8("Battle of Hoth",                DEFAULT=3),
        UInt8("Escape from Echo Base",         DEFAULT=3),
        UInt8("The Asteroid Field",            DEFAULT=3),
        UInt8("Ord Mantell Junkyard",          DEFAULT=3),
        UInt8("Gall Spaceport",                DEFAULT=3),
        UInt8("Mos Eisley and Beggars Canyon", DEFAULT=3),
        UInt8("Imperial Freighter Suprosa",    DEFAULT=3),
        UInt8("Sewers of the Imperial City",   DEFAULT=3),
        UInt8("Xizors Palace",                 DEFAULT=3),
        UInt8("Skyhook Battle",                DEFAULT=3),
        SIZE=10
        ),
    Struct("ammo counts", 
        Struct("Battle of Hoth",                INCLUDE=weapons),
        Struct("Escape from Echo Base",         INCLUDE=weapons),
        Struct("The Asteroid Field",            INCLUDE=weapons),
        Struct("Ord Mantell Junkyard",          INCLUDE=weapons),
        Struct("Gall Spaceport",                INCLUDE=weapons),
        Struct("Mos Eisley and Beggars Canyon", INCLUDE=weapons),
        Struct("Imperial Freighter Suprosa",    INCLUDE=weapons),
        Struct("Sewers of the Imperial City",   INCLUDE=weapons),
        Struct("Xizors Palace",                 INCLUDE=weapons),
        Struct("Skyhook Battle",                INCLUDE=weapons),
        SIZE=50
        ),
    Pad(1),
    Struct("completion times",
         #measured in seconds
         BUInt16("Battle of Hoth"),
         BUInt16("Escape from Echo Base"),
         BUInt16("The Asteroid Field"),
         BUInt16("Ord Mantell Junkyard"),
         BUInt16("Gall Spaceport"),
         BUInt16("Mos Eisley and Beggars Canyon"),
         BUInt16("Imperial Freighter Suprosa"),
         BUInt16("Sewers of the Imperial City"),
         BUInt16("Xizors Palace"),
         BUInt16("Skyhook Battle"),
         SIZE=20
         ),
    Struct("challenge points",
         UInt8("Battle of Hoth",                MIN=0, MAX=3 ),
         UInt8("Escape from Echo Base",         MIN=0, MAX=10),
         UInt8("The Asteroid Field",            MIN=0, MAX=6 ),
         UInt8("Ord Mantell Junkyard",          MIN=0, MAX=12),
         UInt8("Gall Spaceport",                MIN=0, MAX=15),
         UInt8("Mos Eisley and Beggars Canyon", MIN=0, MAX=12),
         UInt8("Imperial Freighter Suprosa",    MIN=0, MAX=10),
         UInt8("Sewers of the Imperial City",   MIN=0, MAX=9 ),
         UInt8("Xizors Palace",                 MIN=0, MAX=10),
         UInt8("Skyhook Battle",                MIN=0, MAX=0 ),
         SIZE=10
         ),
    #OR-ing this value with the first checksum byte must
    #produce 255, b'\xff'. If it doesnt then the save is
    #considered corrupt and is erased. The first checksum
    #byte will be defaulted to 0, and this one to 255.
    UInt8("file checksum 2", DEFAULT=255, EDITABLE=False),
    Pad(1)
    )

sote_rep_def = TagDef(
    UInt8("eep checksum 1", EDITABLE=False),
    BytesRaw("header magic 1", EDITABLE=False, SIZE=4, DEFAULT=HEADER_MAGIC_1),
    UEnum8("file just beaten",
        "none",
        "file 1",
        "file 2",
        "file 3",
        "file 4"
        ),
    Array("saves", SIZE=4, SUB_STRUCT=save_file, MIN=4, MAX=4),
    BytesRaw("header magic 2", EDITABLE=False, SIZE=3, DEFAULT=HEADER_MAGIC_2),

    #OR-ing this value with the first checksum byte must produce 255, b'\xff'.
    #If it doesnt then the save is considered corrupt and is erased.
    #The first checksum byte will be defaulted to 0, and this one to 255.
    UInt8("eep checksum 2", DEFAULT=255, EDITABLE=False),
    Pad(14),
    
    GUI_NAME="sote eep save file",
    ext=".eep", def_id="sote_eep_save", make_gui_names = True
    )

