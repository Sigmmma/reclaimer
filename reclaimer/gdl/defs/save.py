from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *

def get(): return gdl_savemeta_def

def levels_bool(name, count):
    bools = []
    for i in range(count-1):
        bools.append('level %s unlocked'%(i+2))
    bools.append('realm beaten')
    return Bool8(name, *bools)

p_attrs = Struct('character attrs',
    SInt32('exp', GUI_NAME='experience'),
    Float('health'),
    Float('strength added'),
    Float('armor added'),
    Float('magic added'),
    Float('speed added'),
    )

p_stats = Struct('character stats',
    SInt32('enemies killed'),
    SInt32('generals killed'),
    SInt32('golems killed'),
    SInt32('bosses killed'),
    SInt32('generators destroyed'),
    SInt32('gold found'),
    Float('total playtime'),
    )

p_powerup = Struct('character powerup',
    Float('time left'),
    SEnum32('type'),#need these enums
    Float('attribute add'),
    Bool32('special flags'),#need these flags
    )

p_stuff = Container('character stuff',
    SInt16('potions'),
    SInt16('keys'),
    Bool16('shards',
        #this part is not likely 100% accurate. most of it feels like it is tho
        ('lich shard',1<<1),
        ('dragon shard',1<<2),
           
        ('chimera shard',1<<3),
        ('plague shard',1<<4),
        ('drider shard',1<<5),
           
        ('djinn shard',1<<6),
        ('yeti shard',1<<7),
        ('wraith shard',1<<8),
        ('unknown1',1<<9),
        ('unknown2',1<<10),
        ),
    Bool16('runes',
        #this is completely accurate I believe
        'blue 1',
        'blue 2',
        'blue 3',
        'red 1',
        'red 2',
        'red 3',
        'yellow 1',
        'yellow 2',
        'yellow 3',
        'green 1',
        'green 2',
        'green 3',
        'final rune',
        ),
    Bool16('legend items',
        #the only one I know is accurate is the parchment
        ('unknown1',1<<1),
        ('unknown2',1<<2),
        ('unknown3',1<<3),

        ('unknown4',1<<7),
        ('unknown5',1<<8),
        ('parchment',1<<9),
        ('unknown6',1<<10),
        ('unknown7',1<<11),
        #('book',1<<),
        #('scimitar',1<<),
        #('javelin',1<<),
        #('bellows',1<<),
        #('lamp',1<<),
        #('lantern',1<<),
        #('soul savior',1<<),
           
        #[ mask:0x1,   unknown0,  False ]
        #[ mask:0x2,   unknown1,  True ]
        #[ mask:0x4,   unknown2,  True ]
        #[ mask:0x8,   unknown3,  True ]
        #[ mask:0x10,  unknown4,  False ]
        #[ mask:0x20,  unknown5,  False ]
        #[ mask:0x40,  unknown6,  False ]
        #[ mask:0x80,  unknown7,  True ]
        #[ mask:0x100, unknown8,  False ]
        #[ mask:0x200, parchment, True ]
        #[ mask:0x400, unknown10, True ]
        #[ mask:0x800, unknown11, True ]
        #only missing soul savior and toxic bellows
        ),
    SInt16('powerup count'),

    UInt16('rune attempt1'),
    UInt16('rune attempt2'),
    UInt16('legend attempt1'),
    UInt16('legend attempt2'),
    UInt16('boss attempt1'),
    UInt16('boss attempt2'),

    Struct('gargoyle items',
        LSInt16('fangs'),
        LSInt16('feathers'),
        LSInt16('claws'),
        ),
    Pad(2),
    Struct('crystals',
        LSInt16('town'),
        LSInt16('mountain'),
        LSInt16('castle'),
        LSInt16('sky'),
        LSInt16('forest'),
        LSInt16('desert'),
        LSInt16('ice'),
        LSInt16('dream'),
        ),
    UInt32('gold'),
    Array('powerups', SUB_STRUCT=p_powerup, SIZE=32),
    UInt8Array('powerup states', SIZE=32),
    )

p_waves = Struct('levels',
    Pad(1),
    levels_bool('castle realm',6),
    levels_bool('mountain realm',6),
    levels_bool('desert realm',5),
    levels_bool('forest realm',5),#not sure
    levels_bool('temple',2),#not sure
    levels_bool('underworld',2),#not sure
    levels_bool('town realm',5),#not sure
    levels_bool('battlefields',3),#not sure
    levels_bool('ice realm',5),
    levels_bool('dream realm',6),
    levels_bool('sky realm',5),#not sure
    #this next one seems to be wrong, but I'm leavign it here for tweaking
    Bool8('barriers down',
        'sky',
        'dream',
        'castle',
        'town',
        'ice',
        'desert',
        'forest',
        'mountain',
        ),
    Pad(1),
    )

gdl_savemeta_def = TagDef(
    Pad(20),
    StrLatin1('name', SIZE=7),
    Pad(1),
    SEnum16('last alt type',
        "warrior", "valkyrie", "wizard",    "archer",
        "dwarf",   "knight",   "sorceress", "jester",

        "minotaur", "falconess", "jackal", "tigress",
        "ogre",     "unicorn",   "medusa", "hyena",
        "sumner",
        ),
    SEnum8('last color',
        "yellow",
        "blue",
        "red",
        "green",
        ),
                
    SInt8('char saved'),
    Bool16('class unlocks',
        "minotaur",
        "falconess",
        "jackal",
        "tigress",
        "ogre",
        "unicorn",
        "medusa",
        "hyena",
        "sumner",
        ),
    UInt16('level total'),
    
    Array('character attributes', SUB_STRUCT=p_attrs, SIZE=16),
    Array('character stats', SUB_STRUCT=p_stats, SIZE=16),
    Array('character stuff', SUB_STRUCT=p_stuff, SIZE=16),
    Array('character levels', SUB_STRUCT=p_waves, SIZE=16),
    
    UEnum8('control scheme',
        "ps2",
        "arcade",
        "robotron",
        "one handed",
        ),
    UEnum8('rumble',
        "none",
        "light",
        "medium",
        "maximum",
        ),
    UEnum8('auto-attack',
        "off",
        "on",
        ),
    UEnum8('auto-aim',
        "off",
        "on",
        ),
    UInt8Array('help disp', SIZE=256),
    
    NAME='gdl game save',
    ext=".xsv", def_id="save", endian='<',
    )
