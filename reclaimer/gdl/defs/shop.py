from supyr_struct.defs.tag_def import TagDef
from ..common_descs import *
from ..field_types import *

def get(): return shop_def

item_type = LUEnum32('type',
    ('exit',   0),
    ('key',    1),
    ('potion', 3),

    ('ten strength', 5),
    ('ten speed', 6),
    ('ten armor', 7),
    ('ten magic', 8),

    ('reflect shield',  9),
    ('phoenix',        10),
    ('rapid fire',     11),
    ('three way shot', 12),
    ('five way shot',  34),

    ('hammer',        13),
    ('elec shield',   14),
    ('fire shield',   15),

    ('food',     17),
    ('levitate', 18),
    ('growth',   19),
    ('growth2',  4),
    ('speed', 28),
    ('enemy shrink', 29),

    ('fire amulet',  20),
    ('elec amulet',  21),
    ('light amulet', 22),
    ('acid amulet',  23),

    ('super shot', 24),

    ('fire breath', 25),
    ('lightning breath', 26),
    ('acid breath',  27),

    ('invisibility', 30),
    ('invulnerable', 31),
    ('gold invulnerable', 16),
    ('x-ray',    32),
    ('gas mask', 33),

    ('anti-death', 35),
    ('hand-of-death', 36),
    ('health vampire', 37),
    ('mikey dummy', 38),
    #the next 20 items after 38 act like exit,
    #so im assuming all other values do as well
    )

item = Struct('item',
    StrLatin1('icon id',     SIZE=32),
    StrLatin1('description', SIZE=32),
    LFloat('scale', DEFAULT=1.0),
    item_type,
    LUInt32('price'),
    LUInt32('amount'),
    SIZE=80,
    )

item_array = Lump('items',
    SUB_STRUCT=item, SIZE=lump_size, POINTER=lump_pointer
    )

shop_def = TagDef("shop",
    Struct('wad header',
        LUInt32('lump headers pointer'),
        LUInt32('lump count', DEFAULT=1),
        Pad(8),
        ),
    lump_headers,

    #these need to be in a container to have the same index
    #ordering as their headers in the lump_headers array
    Container('lumps',
        item_array
    ),

    ext=".wad"
    )
