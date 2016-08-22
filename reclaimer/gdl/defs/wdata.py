from supyr_struct.defs.tag_def import TagDef
from ..common_descs import *
from ..fields import *

def get(): return wdata_def

lump_kw = {SIZE:lump_size, POINTER:lump_pointer}

#############################
'''individual lump structs'''
#############################

'''lump block arrays'''
player_datas = Lump('',
    SUB_STRUCT=None, **lump_kw
    )

wdata_def = TagDef("wdata",
    QStruct('wad header',
        LUInt32('lump headers pointer'),
        LUInt32('lump count', DEFAULT=8),
        Pad(8),
        ),
    lump_headers,

    #these need to be in a container to have the same index
    #ordering as their headers in the lump_headers array
    Container('lumps'),

    ext=".wad"
    )
