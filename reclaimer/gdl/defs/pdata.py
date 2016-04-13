from supyr_struct.defs.tag_def import TagDef
from ..common_descriptors import *
from ..fields import *

def get(): return pdata_def

lump_kw = {SIZE:lump_size, POINTER:lump_pointer}

#############################
'''individual lump structs'''
#############################

effect = Struct('effect',
    LBool32('flags'),
    LSInt32('next fx index'),
    LSInt32('fx index'),
    LSInt32('snd index'),
    StrLatin1('fx desc', SIZE=16),
    StrLatin1('snd desc', SIZE=16),
    LSInt16('zmod'),
    LSInt16('alpha mod'),
    Struct('offset', INCLUDE=X_Y_Z_Float),
    LFloat('max len'),
    LFloat('radius'),
    LFloat('scale'),
    Struct('color',
           UInt8('b'),
           UInt8('g'),
           UInt8('r'),
           UInt8('a'),
           ),
    SIZE=80,
    )

damage = Struct('damage',
    LSInt16('type'),
    LBool16('flags'),
    LSEnum32('damage type'),
    LFloat('hit rad'),
    LFloat('radius'),
    LFloat('min rad'),
    LFloat('delay'),
    LFloat('min time'),
    LFloat('max time'),
    LFloat('angle'),
    LFloat('arc'),
    LFloat('pitch'),
    Struct('offset', INCLUDE=X_Y_Z_Float),
    LFloat('amount'),
    LFloat('speed min'),
    LFloat('speed max'),
    LFloat('weight'),
    LSInt16('fx index'),
    LSInt16('hit fx index'),
    LSInt16('loop fx index'),
    LSInt16('next'),
    LSInt16('start frame'),
    LSInt16('end frame'),
    LSInt16('help index'),
    LSInt16('dummy'),
    )

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

    LFloat('strength min'),
    LFloat('strength max'),
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
    Struct('weapon offset',   INCLUDE=X_Y_Z_Float),
    Array('weapon fx offsets', SIZE=10, SUB_STRUCT = X_Y_Z_Float),
    Array('weapon fx scales',  SIZE=10, SUB_STRUCT = X_Y_Z_Float),
    Struct('turboA offset',   INCLUDE=X_Y_Z_Float),
    Struct('familiar offset', INCLUDE=X_Y_Z_Float),
    Struct('fam proj offset', INCLUDE=X_Y_Z_Float),
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

pdata_def = TagDef(
    rom_header,
    lump_headers,

    #these need to be in a container to have the same index
    #ordering as their headers in the lump_headers array
    Container('lumps',
        effects,
        damages,
        player_datas,
    ),
    
    NAME='gdl player data',
    ext=".wad", def_id="pdata"
    )
