from supyr_struct.defs.tag_def import TagDef
from ..common_descriptors import *
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

wdata_def = TagDef(
    rom_header,
    lump_headers,

    #these need to be in a container to have the same index
    #ordering as their headers in the lump_headers array
    Container('lumps',
    ),
    
    NAME='gdl world data',
    ext=".wad", def_id="wdata"
    )
