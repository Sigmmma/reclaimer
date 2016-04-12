from supyr_struct.defs.common_descriptors import *
from .fields import *

def lump_fcc(value):
    return fcc(value, 'big')

def find_index(parent, block):
    '''Need a custom function that checks the id of a
    block to find which index it's in. list.index()
    decides on a match by content rather than id().'''
    block_id = id(block)
    for i in range(len(parent)):
        if id(list.__getitem__(parent, i)) == block_id:
            return i
    return None
    

def get_lump_type(block=None, parent=None, attr_index=None,
                  rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if attr_index is None:
        attr_index = find_index(parent, block)
    if parent is None or attr_index is None:
        raise KeyError
    return parent.get_tag().data.lump_headers[attr_index].lump_id.data_name

def lump_size(block=None, parent=None, attr_index=None,
              rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if attr_index is None:
        attr_index = find_index(parent, block)
    if parent is None or attr_index is None:
        return 0
    header = parent.get_tag().data.lump_headers[attr_index]
    if new_value is None:
        return header.lump_array_length
    header.lump_array_length = new_value

def lump_pointer(block=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if attr_index is None:
        attr_index = find_index(parent, block)
    if parent is None or attr_index is None:
        return 0
    header = parent.get_tag().data.lump_headers[attr_index]
    if new_value is None:
        return header.lump_array_pointer
    header.lump_array_pointer = new_value


#############################
'''main wad header structs'''
#############################
rom_header = Struct('rom header',
    LUInt32('lump headers pointer'),
    LUInt32('lump count'),
    Pad(8),
    )

lump_header = Struct('lump header',
    LUEnum32('lump id',
        #TEXT wad lump values
        ('FONT', lump_fcc('FONT'), 'font' ),
        ('TEXT', lump_fcc('TEXT'), 'string text'),
        ('DEFS', lump_fcc('DEFS'), 'def names text'),

        ('TOFF', lump_fcc('TOFF'), 'string offsets'),
        ('LOFF', lump_fcc('LOFF'), 'list offsets'),
        ('SDEF', lump_fcc('SDEF'), 'string def offsets'),
        ('LDEF', lump_fcc('LDEF'), 'list def offsets'),

        ('LIST', lump_fcc('LIST'), 'string list'),
        ('STRS', lump_fcc('STRS'), 'string message'),
        
        #PDATA wad lump values
        ('SFXX', lump_fcc('SFXX'), 'player sound fx'),
        ('DAMG', lump_fcc('DAMG'), 'player attack damage'),
        ('PDAT', lump_fcc('PDAT'), 'player character data'),
             
        #WDATA wad lump values
        ('ENMY', lump_fcc('ENMY'), 'enemy type'),
        ('BCAM', lump_fcc('BCAM'), 'boss camera'),
        ('CAMS', lump_fcc('CAMS'), 'cameras'),
        ('SNDS', lump_fcc('SNDS'), 'sounds'),
        ('AUDS', lump_fcc('AUDS'), 'audio streams'),
        ('MAPS', lump_fcc('MAPS'), 'maps?'),
        ('LEVL', lump_fcc('LEVL'), 'level details'),
        ('WRLD', lump_fcc('WRLD'), 'world description'),
             
        #SHPDATA wad lump values
        ('ITEM', lump_fcc('ITEM'), 'shop items'),
        ),
    LPointer32('lump array pointer'),
    LUInt32('lump array length'),
    LUInt32('lump array length2'),
    )

lump_headers = Array('lump headers',
    POINTER='.rom_header.lump_headers_pointer',
    SIZE='.rom_header.lump_count', SUB_STRUCT=lump_header,
    )

'''these are unused because it is just too
annoying to deal with lumps with a switch'''
#lump_switch = Switch('lump',
#    CASE=get_lump_type,
#    CASES={'TOFF':string_offsets,
#           'LOFF':list_offsets,
#           'SDEF':string_def_offsets,
#           'LDEF':list_def_offsets,
#           
#           'LIST':string_list_array,
#           'STRS':string_message_array,
#
#           'FONT':font_array,
#           'TEXT':raw_text,
#           'DEFS':raw_def_names,
#           },
#    )
#
#lumps = Array('lumps',
#    SIZE='.rom_header.lump_count', SUB_STRUCT=lump_switch,
#    )
