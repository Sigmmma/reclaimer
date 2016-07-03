from array import array

from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from . import xbe
from .objs.save import GdlSaveTag

def get(): return gdl_savemeta_def

def levels_bool(name, count):
    bools = []
    for i in range(count-1):
        bools.append('level %s beaten'%(i+1))
    bools.append('boss beaten')
    return Bool8(name, *bools)

help_disp_default = array('B', [0]*256)
for i in (0,1,2,6,7,8,11,15,16,17,20,21,22,27,28,32,35,37,
          41,42,44,45,48,51,53,58,60,61,67,82,83,87,88,92,
          102,110,111,113,125,126,130,132,134,135,137):
    help_disp_default[i] = 0x11

char_names = (
    "warrior",  "valkyrie",  "wizard",    "archer",
    "dwarf",    "knight",    "sorceress", "jester",
    "minotaur", "falconess", "jackal",    "tigress",
    "ogre",     "unicorn",   "medusa",    "hyena")

def make_name_map(suffix=''):
    name_map = {}
    for i in range(len(char_names)):
        name_map[char_names[i]+suffix] = i
    return name_map

special_flags = xbe.special_types
armor_flags   = xbe.armor_types
weapon_flags  = xbe.weapon_types
no_flags = LBool32('flags')

runes = (
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
    )

legend_items = (
    Pad(1),
    'scimitar',
    'ice axe',
    'lamp',
    'bellows',
    'savior',
    Pad(1),
    'book',
    Pad(1),
    'parchment',
    'lantern',
    'javelin',
    )

p_attrs = Struct('character attrs',
    SInt32('exp', GUI_NAME='experience'),
    Float('health'),
    Float('fight added'),
    Float('armor added'),
    Float('magic added'),
    Float('speed added'),
    SIZE=24,
    )

p_stats = Struct('character stats',
    SInt32('enemies killed'),
    SInt32('generals killed'),
    SInt32('golems killed'),
    SInt32('bosses killed'),
    SInt32('generators destroyed'),
    SInt32('gold found'),
    Float('total playtime'),#counted in frames
    SIZE=28,
    )

p_powerup = Struct('character powerup',
    Float('time left'),
    SEnum32('type',
        "none",
        Pad(4),
        "weapon",
        "armor",
        "speed",
        "magic",
        "special",
        ),
    Float('attribute add'),
    Union("flags",
        CASE='.type.enum_name',
        CASES={'weapon': weapon_flags,
               'armor': armor_flags,
               'special': special_flags}
        ),
    SIZE=16,
    )

p_stuff = Container('character stuff',
    SInt16('potions'),
    SInt16('keys'),
    Bool16('shards',
        Pad(1),
        'lich shard',
        'dragon shard',
        'chimera shard',
        'plague shard',
        'drider shard',
        'djinn shard',
        'yeti shard',
        'wraith shard',
        #'unknown1',
        #'unknown2',
        ),
    Bool16('runes', *runes),
    Bool16('legend items', *legend_items),
    SInt16('powerup count'),

    Bool16('rune attempts sp', *runes),
    Bool16('rune attempts mp', *runes),
    Bool16('legend attempts sp', *legend_items),
    Bool16('legend attempts mp', *legend_items),
    #boss_attempts 1 and 2 are always 0 it seems, so rather
    #than have them editable, lets just treat them as padding
    #UInt16('boss attempts 1'),
    #UInt16('boss attempts 2'),
    Pad(4),

    Struct('gargoyle items',
        # a value of -1 means all that the max amount have been collected
        LSInt16('fangs'),
        LSInt16('feathers'),
        LSInt16('claws'),
        ),
    Pad(2),#the shell3d.pdb lied about this padding. it tried to say
    #       that it's after the crystals, not before it. it isn't.
    Struct('crystals',
        # a value of -1 means all that the max amount have been collected
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
    SIZE=596,
    )


p_waves = Struct('levels',
    Pad(1),
    levels_bool('castle realm',6),
    levels_bool('mountain realm',6),
    levels_bool('desert realm',5),
    levels_bool('forest realm',5),
    levels_bool('temple',2),
    levels_bool('underworld',2),
    levels_bool('town realm',5),
    levels_bool('battlefields',4),
    levels_bool('ice realm',5),
    levels_bool('dream realm',6),
    levels_bool('sky realm',5),
    Bool8('unknown',
        'unknown0',
        'unknown1',
        'unknown2',
        'unknown3',
        'unknown4',
        'unknown5',
        'unknown6',
        'unknown7',
        ),
    Pad(1),
    )

gdl_savemeta_def = TagDef("save",
    BytesRaw('hmac_sig', SIZE=20),
    Container('save data',
        StrLatin1('name', SIZE=7, DEFAULT='PLAYER'),
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
        
        Array('character attrs',  SUB_STRUCT=p_attrs,
            SIZE=16, NAME_MAP=make_name_map('_attrs')),
        Array('character stats',  SUB_STRUCT=p_stats,
            SIZE=16, NAME_MAP=make_name_map('_stats')),
        Array('character stuff',  SUB_STRUCT=p_stuff,
            SIZE=16, NAME_MAP=make_name_map('_stuff')),
        Array('character levels', SUB_STRUCT=p_waves,
            SIZE=16, NAME_MAP=make_name_map('_levels')),
        
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
            DEFAULT=2,
            ),
        UEnum8('auto-attack',
            "off",
            "on",
            DEFAULT=1,
            ),
        UEnum8('auto-aim',
            "off",
            "on",
            DEFAULT=1,
            ),
        #The only values that seem to be in the help_disp
        #array are either 0x00, 0x10, or 0x11.
        #
        #These might be enumerators designating the display
        #status of each help hint text(invisible, visible, seen)
        #
        #New files have 
        UInt8Array('help disp', SIZE=256, DEFAULT=help_disp_default),
        ),

    ext=".xsv", endian='<', tag_cls=GdlSaveTag,
    )
