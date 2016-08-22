from supyr_struct.defs.common_descs import *

from .fields import *

def lump_fcc(value):
    return fcc(value, 'big')    

def get_lump_type(block=None, parent=None, attr_index=None,
                  rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.parent
    if attr_index is None:
        attr_index = parent.index_by_id(block)
    return parent.get_root().data.lump_headers[attr_index].lump_id.enum_name

def lump_size(block=None, parent=None, attr_index=None,
              rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.parent
    if parent is None:
        return 0
    if attr_index is None:
        try:
            attr_index = parent.index_by_id(block)
        except ValueError:
            return 0

    try:
        header = parent.get_root().data.lump_headers[attr_index]
    except IndexError:
        return 0
    if new_value is None:
        return header.lump_array_length
    header.lump_array_length = new_value

def lump_pointer(block=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.parent
    if parent is None:
        return 0
    if attr_index is None:
        try:
            attr_index = parent.index_by_id(block)
        except ValueError:
            return 0
    try:
        header = parent.get_root().data.lump_headers[attr_index]
    except IndexError:
        return 0
    if new_value is None:
        return header.lump_array_pointer
    header.lump_array_pointer = new_value

# used in a lot of places
xyz_float = QStruct('xyz_float',
    Float("x"),
    Float("y"),
    Float("z")
    )

#############################
'''individual lump structs'''
#############################

effect = Struct('effect',
    LBool32('flags',
        "unknown0",  "unknown1",  "unknown2",  "unknown3",
        "unknown4",  "unknown5",  "unknown6",  "unknown7",
        "unknown8",  "unknown9",  "unknown10", "unknown11",
        "unknown12", "unknown13", "unknown14", "unknown15",
        "unknown16", "unknown17", "unknown18", "unknown19",
        "unknown20", "unknown21", "unknown22", "unknown23",
        "unknown24", "unknown25", "unknown26", "unknown27",
        "unknown28", "unknown29", "unknown30", "unknown31"
        ),
    LSInt32('next fx index'),
    LSInt32('fx index'),
    LSInt32('snd index'),
    StrLatin1('fx desc', SIZE=16),
    StrLatin1('snd desc', SIZE=16),
    LSInt16('zmod'),
    LSInt16('alpha mod'),
    QStruct('offset', INCLUDE=xyz_float),
    LFloat('max len'),
    LFloat('radius'),
    LFloat('scale'),
    QStruct('color',
           UInt8('b'),
           UInt8('g'),
           UInt8('r'),
           UInt8('a'),
           ),
    SIZE=80,
    )

damage = Struct('damage',
    LUEnum16("type"),
    LBool16("flags",
        "unknown0",  "unknown1",  "unknown2",  "unknown3",
        "unknown4",  "unknown5",  "unknown6",  "unknown7",
        "unknown8",  "unknown9",  "unknown10", "unknown11",
        "unknown12", "unknown13", "unknown14", "unknown15",
        ),
    LBitStruct('damage type',
        BitUEnum('type',
            "normal",
            "fire",
            "elec",
            "light",
            "acid",
            SIZE=4,
            ),
        BitBool('flags',
            'knockback',
            'knockdown',
            'blownaway',
            'stun',
            'knockover',
            'magic',
            'explode',
            'poisongas',
            'deathstun',
            'spike',
            'grabbed',
            'thrown',
            'whirlwind',
            'arrow',
            'fball',
            'three way',
            'super',
            'reflect', 
            'five way',
            'heals',
            'nohitfx',
            'turbo',
            'sticky',
            'bosshit',
            'hammer',
            'rapid',
            'low',
            SIZE=28,
            ),
        SIZE=4,
        ),
    LFloat('hit rad'),
    LFloat('radius'),
    LFloat('min rad'),
    LFloat('delay'),
    LFloat('min time'),
    LFloat('max time'),
    LFloat('angle'),
    LFloat('arc'),
    LFloat('pitch'),
    QStruct('offset', INCLUDE=xyz_float),
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
wad_header = QStruct('wad header',
    LUInt32('lump headers pointer'),
    LUInt32('lump count'),
    Pad(8),
    )

lump_header = Struct('lump header',
    LUEnum32('lump id',
        #text wad lump values
        {NAME:'font', VALUE:lump_fcc('FONT'), GUI_NAME:'font'},
        {NAME:'text', VALUE:lump_fcc('TEXT'), GUI_NAME:'string text'},
        {NAME:'defs', VALUE:lump_fcc('DEFS'), GUI_NAME:'def names text'},

        {NAME:'toff', VALUE:lump_fcc('TOFF'), GUI_NAME:'string offsets'},
        {NAME:'loff', VALUE:lump_fcc('LOFF'), GUI_NAME:'list offsets'},
        {NAME:'sdef', VALUE:lump_fcc('SDEF'), GUI_NAME:'string def offsets'},
        {NAME:'ldef', VALUE:lump_fcc('LDEF'), GUI_NAME:'list def offsets'},

        {NAME:'list', VALUE:lump_fcc('LIST'), GUI_NAME:'string list'},
        {NAME:'strs', VALUE:lump_fcc('STRS'), GUI_NAME:'string message'},
        
        #pdata and critter wad lump values
        {NAME:'sfxx', VALUE:lump_fcc('SFXX'), GUI_NAME:'sound/visual fx'},
        {NAME:'damg', VALUE:lump_fcc('DAMG'), GUI_NAME:'attack damage'},
             
        #critter wad lump values
        {NAME:'desc', VALUE:lump_fcc('DESC'), GUI_NAME:'????'},
        {NAME:'adda', VALUE:lump_fcc('ADDA'), GUI_NAME:'????'},
        {NAME:'node', VALUE:lump_fcc('NODE'), GUI_NAME:'????'},
        {NAME:'move', VALUE:lump_fcc('MOVE'), GUI_NAME:'????'},
        {NAME:'ptrn', VALUE:lump_fcc('PTRN'), GUI_NAME:'????'},
        {NAME:'type', VALUE:lump_fcc('TYPE'), GUI_NAME:'????'},
             
        #pdata wad lump values
        {NAME:'pdat', VALUE:lump_fcc('PDAT'), GUI_NAME:'player data'},
             
        #wdata wad lump values
        {NAME:'enmy', VALUE:lump_fcc('ENMY'), GUI_NAME:'enemy type'},
        {NAME:'bcam', VALUE:lump_fcc('BCAM'), GUI_NAME:'boss camera'},
        {NAME:'cams', VALUE:lump_fcc('CAMS'), GUI_NAME:'cameras'},
        {NAME:'snds', VALUE:lump_fcc('SNDS'), GUI_NAME:'sounds'},
        {NAME:'auds', VALUE:lump_fcc('AUDS'), GUI_NAME:'audio streams'},
        {NAME:'maps', VALUE:lump_fcc('MAPS'), GUI_NAME:'maps'},
        {NAME:'levl', VALUE:lump_fcc('LEVL'), GUI_NAME:'level details'},
        {NAME:'wrld', VALUE:lump_fcc('WRLD'), GUI_NAME:'world description'},
             
        #shpdata wad lump values
        {NAME:'item', VALUE:lump_fcc('ITEM'), GUI_NAME:'shop items'},
        ),
    LPointer32('lump array pointer'),
    LUInt32('lump array length'),
    LUInt32('lump array length2'),
    )

lump_headers = Array('lump headers',
    POINTER='.wad_header.lump_headers_pointer',
    SIZE='.wad_header.lump_count', SUB_STRUCT=lump_header,
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
#    SIZE='.wad_header.lump_count', SUB_STRUCT=lump_switch,
#    )
