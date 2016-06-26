from supyr_struct.defs.tag_def import TagDef
from ..common_descriptors import *
from ..fields import *

def get(): return pdata_def

lump_kw = {SIZE:lump_size, POINTER:lump_pointer}

#############################
'''individual lump structs'''
#############################

player_data = Container('player data',
    LSInt16('num sfx'),
    LSInt16('num damage'),
    LPointer32('plyr sfx'),
    LPointer32('plyr damage'),

    LSInt16('turboA close'),
    LSInt16('turboA low'),
    LSInt16('turboA step'),
    LSInt16('turboA 360'),
    LSInt16('turboA throw'),
    LSInt16('turboB'),
    LSInt16('turboC1'),
    LSInt16('turboC2'),
    LSInt16('combo1'),
    LSInt16('combo2'),
    LSInt16('combo hit'),
    LSInt16('victory'),
    LSInt32('init flag'),

    LFloat('fight min'),
    LFloat('fight max'),
    LFloat('speed min'),
    LFloat('speed max'),
    LFloat('armor min'),
    LFloat('armor max'),
    LFloat('magic min'),
    LFloat('magic max'),

    LFloat('height'),
    LFloat('width'),
    LFloat('attny'),
    LFloat('coly'),
    LFloat('powerup time'),
    Struct('weapon offset',   INCLUDE=xyz_float),
    Array('weapon fx offsets', SIZE=10, SUB_STRUCT=xyz_float),
    Array('weapon fx scales',  SIZE=10, SUB_STRUCT=xyz_float),
    Struct('turboA offset',   INCLUDE=xyz_float),
    Struct('familiar offset', INCLUDE=xyz_float),
    Struct('fam proj offset', INCLUDE=xyz_float),
    LFloat('streak fwd mul'),
    )


'''lump block arrays'''
effects = Lump('effects',
    SUB_STRUCT=effect, **lump_kw
    )
damages = Lump('damages',
    SUB_STRUCT=damage, **lump_kw
    )
player_datas = Lump('player datas',
    SUB_STRUCT=player_data, **lump_kw
    )

pdata_def = TagDef("pdata",
    rom_header,
    lump_headers,

    #these need to be in a container to have the same index
    #ordering as their headers in the lump_headers array
    Container('lumps',
        effects,
        damages,
        player_datas,
        ),

    ext=".wad",
    )
