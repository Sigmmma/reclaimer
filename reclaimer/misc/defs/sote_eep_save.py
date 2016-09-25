from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descs import *
from supyr_struct.field_types import *

HEADER_MAGIC_1 = b'\xFF\x53\x68\x26'
HEADER_MAGIC_2 = HEADER_MAGIC_1[1:]

def get(): return sote_eep_def

weapons = QStruct( "weapons",
    UInt8("pulse"),
    UInt8("flame"),
    UInt8("seeker"),
    UInt8("stunner"),
    UInt8("disruptor")
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
        "battle of hoth",
        "escape from echo base",
        "the asteroid field",
        "ord mantell junkyard",
        "gall spaceport",
        "mos eisley and beggars canyon",
        "imperial freighter suprosa",
        "sewers of the imperial city",
        "xizors palace",
        "skyhook battle"
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
            SIZE=2),
        Pad(2),
        BitUEnum("sound panning",
            "stereo",
            "mono",
            SIZE=1),
        Pad(3),
        #byte 2
        Bit("seeker camera off"),
        Pad(3),
        BitUEnum("sfx volume", 
            "loud",
            "medium",
            "soft",
            "off",
            SIZE=2),
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
    QStruct("extra lives",
        UInt8("battle of hoth",                DEFAULT=3),
        UInt8("escape from echo base",         DEFAULT=3),
        UInt8("the asteroid field",            DEFAULT=3),
        UInt8("ord mantell junkyard",          DEFAULT=3),
        UInt8("gall spaceport",                DEFAULT=3),
        UInt8("mos eisley and beggars canyon", DEFAULT=3),
        UInt8("imperial freighter suprosa",    DEFAULT=3),
        UInt8("sewers of the imperial city",   DEFAULT=3),
        UInt8("xizors palace",                 DEFAULT=3),
        UInt8("skyhook battle",                DEFAULT=3),
        SIZE=10
        ),
    Struct("ammo counts", 
        QStruct("battle of hoth",                INCLUDE=weapons),
        QStruct("escape from echo base",         INCLUDE=weapons),
        QStruct("the asteroid field",            INCLUDE=weapons),
        QStruct("ord mantell junkyard",          INCLUDE=weapons),
        QStruct("gall spaceport",                INCLUDE=weapons),
        QStruct("mos eisley and beggars canyon", INCLUDE=weapons),
        QStruct("imperial freighter suprosa",    INCLUDE=weapons),
        QStruct("sewers of the imperial city",   INCLUDE=weapons),
        QStruct("xizors palace",                 INCLUDE=weapons),
        QStruct("skyhook battle",                INCLUDE=weapons),
        SIZE=50
        ),
    Pad(1),
    QStruct("completion times",
        #measured in seconds
        BUInt16("battle of hoth"),
        BUInt16("escape from echo base"),
        BUInt16("the asteroid field"),
        BUInt16("ord mantell junkyard"),
        BUInt16("gall spaceport"),
        BUInt16("mos eisley and beggars canyon"),
        BUInt16("imperial freighter suprosa"),
        BUInt16("sewers of the imperial city"),
        BUInt16("xizors palace"),
        BUInt16("skyhook battle"),
        SIZE=20
        ),
    QStruct("challenge points",
        UInt8("battle of hoth",                MIN=0, MAX=3 ),
        UInt8("escape from echo base",         MIN=0, MAX=10),
        UInt8("the asteroid field",            MIN=0, MAX=6 ),
        UInt8("ord mantell junkyard",          MIN=0, MAX=12),
        UInt8("gall spaceport",                MIN=0, MAX=15),
        UInt8("mos eisley and beggars canyon", MIN=0, MAX=12),
        UInt8("imperial freighter suprosa",    MIN=0, MAX=10),
        UInt8("sewers of the imperial city",   MIN=0, MAX=9 ),
        UInt8("xizors palace",                 MIN=0, MAX=10),
        UInt8("skyhook battle",                MIN=0, MAX=0 ),
        SIZE=10
        ),
    #OR-ing this value with the first checksum byte must
    #produce 255, b'\xff'. If it doesnt then the save is
    #considered corrupt and is erased. The first checksum
    #byte will be defaulted to 0, and this one to 255.
    UInt8("file checksum 2", DEFAULT=255, EDITABLE=False),
    Pad(1)
    )

sote_eep_def = TagDef("sote_eep_save",
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

    ext=".eep",
    )

