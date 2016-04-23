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
        #text wad lump values
        ('font', lump_fcc('FONT'), 'font' ),
        ('text', lump_fcc('TEXT'), 'string text'),
        ('defs', lump_fcc('DEFS'), 'def names text'),

        ('toff', lump_fcc('TOFF'), 'string offsets'),
        ('loff', lump_fcc('LOFF'), 'list offsets'),
        ('sdef', lump_fcc('SDEF'), 'string def offsets'),
        ('ldef', lump_fcc('LDEF'), 'list def offsets'),

        ('list', lump_fcc('LIST'), 'string list'),
        ('strs', lump_fcc('STRS'), 'string message'),
        
        #pdata and critter wad lump values
        ('sfxx', lump_fcc('SFXX'), 'sound/visual fx'),
        ('damg', lump_fcc('DAMG'), 'attack damage'),
             
        #critter wad lump values
        ('desc', lump_fcc('DESC'), '????'),
        ('adda', lump_fcc('ADDA'), '????'),
        ('node', lump_fcc('NODE'), '????'),
        ('move', lump_fcc('MOVE'), '????'),
        ('ptrn', lump_fcc('PTRN'), '????'),
        ('type', lump_fcc('TYPE'), '????'),
             
        #pdata wad lump values
        ('pdat', lump_fcc('PDAT'), 'player character data'),
             
        #wdata wad lump values
        ('enmy', lump_fcc('ENMY'), 'enemy type'),
        ('bcam', lump_fcc('BCAM'), 'boss camera'),
        ('cams', lump_fcc('CAMS'), 'cameras'),
        ('snds', lump_fcc('SNDS'), 'sounds'),
        ('auds', lump_fcc('AUDS'), 'audio streams'),
        ('maps', lump_fcc('MAPS'), 'maps'),
        ('levl', lump_fcc('LEVL'), 'level details'),
        ('wrld', lump_fcc('WRLD'), 'world description'),
             
        #shpdata wad lump values
        ('item', lump_fcc('ITEM'), 'shop items'),
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
