from supyr_struct.defs.tag_def import TagDef
from ..common_descriptors import *
from ..fields import *

def get(): return rom_def

def get_text_lump_size(block=None, parent=None, attr_index=None,
                       rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if attr_index is None:
        try:
            attr_index = parent.index(block)
        except ValueError:
            return 0
    if parent is None or attr_index is None:
        return 0
    if new_value is not None:
        return
    lump_headers = parent.get_tag().data.lump_headers
    start = end = lump_headers[attr_index].lump_array_pointer
    
    try:
        end = lump_headers[attr_index+1].lump_array_pointer
    except IndexError:
        if hasattr(rawdata, 'len'):
            end = len(rawdata)
    return end - start

def get_oe_offs_lump_size(block=None, parent=None, attr_index=None,
                          rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if attr_index is None:
        try:
            attr_index = parent.index(block)
        except ValueError:
            return 0
    if parent is None or attr_index is None:
        return 0
    if new_value is not None:
        return
    lump_headers = parent.get_tag().data.lump_headers
    start = end = lump_headers[attr_index].lump_array_pointer
    
    try:
        end = lump_headers[attr_index+1].lump_array_pointer
    except IndexError:
        if hasattr(rawdata, 'len'):
            end = len(rawdata)
    return (end - start)//4

lump_kw         = {SIZE:lump_size,             POINTER:lump_pointer}
text_lump_kw    = {SIZE:get_text_lump_size,    POINTER:lump_pointer}
oe_offs_lump_kw = {SIZE:get_oe_offs_lump_size, POINTER:lump_pointer}

#############################
'''individual lump structs'''
#############################

string_message = Struct('string message',
    #These define which strings(specified by TOFF)
    #are grouped into sets. For example, all of one
    #boss's hints are in one STRS block. "first"
    #specifies which TOFF the grouping starts at
    #Font is the numerical ID of the font to use
    #which should match a FONT block "fontid"
    LSInt32('num',   GUI_NAME='number of strings'),
    LSInt32('first', GUI_NAME='first string index'),
    LSInt32('font id'),
    LFloat('scale'),
    LFloat('sscale'),
    )

string_list = Struct('string list',
    LSInt32('num',   GUI_NAME='number of strings'),
    LSInt32('first', GUI_NAME='first string index'),
    )

font = Struct('font',
    StrLatin1('desc',  GUI_NAME='description', SIZE=16),
    LUInt32('font id', GUI_NAME='id of this font'),
    )

text_data      = BytesRaw('text data',      **text_lump_kw)
def_names_data = BytesRaw('def names data', **text_lump_kw)


'''lump block arrays'''
font_array = Lump('fonts',
    SUB_STRUCT=font, **lump_kw
    )
string_offsets = Lump('string offsets',
    SUB_STRUCT=LUInt32('offset'), **oe_offs_lump_kw
    )
string_message_array = Lump('string messages',
    SUB_STRUCT=string_message, **lump_kw
    )
list_offsets   = Lump('list offsets',
    SUB_STRUCT=LUInt32('offset'), **oe_offs_lump_kw
    )
string_list_array = Lump('string lists',
    SUB_STRUCT=string_list, **lump_kw
    )
#These offsets point to the start of each string list defs name in the DEFS lump
list_def_offsets   = Lump('list def offsets',
    SUB_STRUCT=LUInt32('offset'), **lump_kw
    )
#These offsets point to the start of each string defs name in the DEFS lump
string_def_offsets = Lump('string def offsets',
    SUB_STRUCT=LUInt32('offset'), **lump_kw
    )


rom_def = TagDef(
    rom_header,
    lump_headers,

    #these need to be in a container to have the same index
    #ordering as their headers in the lump_headers array
    Container('lumps',
        font_array,
        text_data,
        string_offsets,
        string_message_array,
        list_offsets,
        string_list_array,
        def_names_data,
        string_def_offsets,
        list_def_offsets,
    ),
    
    NAME='gdl strings resource',
    ext=".rom", def_id="rom"
    )
