from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs.meta_descs import meta_cases
from . objs.map import MapTag

################################################################
################################################################
'''-----------------------   Notes   ---------------------------
    If a tag is located in one of the shared resource maps, the
    offset in tag_header will the the index in the resource
    map that the tag is located in and indexed will be 1.
    To determine which resource map the tag is in, it must be
    done based on the tag class.
    bitm- > bitmaps.map
    snd! -> sounds.map
    font, hmt , str#, ustr -> loc.map

'''
################################################################
################################################################


def get(): return map_def
'''
def map_fcc(value):
    return fcc(value, 'big')

SND__FCC = map_fcc('snd!')

def tag_path_pointer(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    t_head = parent.parent
    m_head = t_head.parent.parent.map_header
    magic = kwargs.get('magic')
    if magic is None:
        magic = PC_INDEX_MAGIC - m_head.tag_index_offset

    #NEED TO FINISH THIS SO IT CAN SET THE PATH POINTER

    if new_value is not None:
        return
    return PC_TAG_INDEX_HEADER_SIZE + t_head.path_offset - magic


def tag_meta_data_pointer(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()

    t_head = parent.parent
    m_head = t_head.parent.parent.map_header
    magic = kwargs.get('magic')
    if magic is None:
        magic =  - m_head.tag_index_offset

    #NEED TO FINISH THIS SO IT CAN SET THE META POINTER

    if new_value is not None:
        return
    return PC_TAG_INDEX_HEADER_SIZE + t_head.meta_offset - magic


def tag_meta_case(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()

    t_head = parent.parent
    if t_head.indexed:
        if t_head.class_1.data == SND__FCC:
            return 'indexed_snd!'
        return

    magic = kwargs.get('magic')
    m_head = t_head.parent.parent.map_header
    if magic is None:
        magic = PC_INDEX_MAGIC - m_head.tag_index_offset

    return t_head.class_1.data
    

def tag_index_array_pointer(node=None, parent=None, new_value=None, **kwargs):
    if node is None:
        raise KeyError()
    b_parent = node.parent

    magic = kwargs.get('magic')
    if magic is None:
        magic = PC_INDEX_MAGIC - b_parent.map_header.tag_index_offset

    if new_value is not None:
        return
    return (PC_TAG_INDEX_HEADER_SIZE +
            b_parent.tag_index_header.index_magic - magic)

tag_meta = Switch("tag meta",
    CASE=tag_meta_case,
    CASES={map_fcc(k): meta_cases[k] for k in meta_cases if len(k) == 4},
    POINTER=tag_meta_data_pointer,
    )


tag_data = Container("tag",
    CStrLatin1("tag path", POINTER=tag_path_pointer),
    tag_meta,
    )
'''
tag_header = Struct("tag header",
    LUEnum32("class 1", GUI_NAME="primary tag class", INCLUDE=valid_tags),
    LUEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_tags),
    LUEnum32("class 3", GUI_NAME="tertiary tag class", INCLUDE=valid_tags),
    LUInt32("id"),
    LUInt32("path offset"),
    LUInt32("meta offset"),
    LUInt32("indexed"),
    # if indexed is 1, the meta_offset is the literal index in the
    # bitmaps, sounds, or loc cache that the meta data is located in.
    Pad(4),
    #STEPTREE=tag_data,
    )

#Apparently the Halo Demo maps have a different
#header as there are 704 bytes #before the header
#that appear to be garbage AND garbage filling
#all the headers null padding.
map_header = Struct("map header",
    LUEnum32('head', ('head', 'head'), EDITABLE=False, DEFAULT='head'),
    LSEnum32("version",
        ("xbox",    5),
        ("pc_demo", 6),
        ("pc_full", 7),
        ("pc_ce", 609),
        ),
    LSInt32("decompressed len"),
    BytesRaw("unknown", SIZE=4),
    LUInt32("tag index offset"),
    LUInt32("tag index meta len"),
    Pad(8),
    ascii_str32("map name"),
    StrLatin1("build date", DEFAULT="01.00.00.0609", EDITABLE=False, SIZE=32),
    LUEnum32("map type",
        "sp",
        "mp",
        "ui",
        ),
    LUInt32("crc32"),
    Pad(1940),
    LUEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    )

tag_index_header_pc = Struct("tag index header",
    LUInt32("index magic", DEFAULT=PC_INDEX_MAGIC),
    LUInt32("base magic"),
    LUInt32("map id"),
    LUInt32("tag count"),

    LUInt32("vertex object count"),
    LUInt32("model raw data offset"),

    LUInt32("indices object count"),
    LUInt32("indices offset"),
    LUInt32("model raw data size"),
    LUEnum32("tag sig", ('tags', 'tags'), EDITABLE=False, DEFAULT='tags'),

    POINTER='.map_header.tag_index_offset', SIZE=40
    )

tag_index = TagIndex("tag index",
    SIZE=".tag_index_header.tag_count",
    WIDGET=DynamicArrayFrame, DYN_NAME_PATH=".STEPTREE.tag_path",
    SUB_STRUCT=tag_header, POINTER=tag_index_array_pointer
    )

subdefs = {}
for key in tag_meta[CASES]:
    #need to make a copy of this, or it screws up the original
    subdefs[key] = dict(tag_meta[CASES][key])
    subdefs[key][POINTER] = tag_meta[POINTER]
        
map_def = TagDef("halo1_pc_map",
    map_header,
    tag_index_header_pc,
    tag_index,

    ext=".map", endian="<", tag_cls=MapTag
    )

map_def.index_magic = PC_INDEX_MAGIC
