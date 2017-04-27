import zlib

from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef
from ..hek.defs.meta_descs import meta_cases

'''
The formula for calculating the magic for ANY map is as follows:
    magic = idx_magic - idx_off

idx_off is the offset of the tag_index_header and idx_magic
varies depending on which engine version the map is for.
To get the idx_magic, do:
    map_magics[map_header.version.enum_name]

where map_magics is in reclaimer.constants

To convert a magic relative pointer to an absolute pointer,
simply do:    abs_pointer = magic_pointer - magic
'''

def tag_path_pointer(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    t_head = parent.parent
    if new_value is not None:
        return
    return t_head.path_offset - kwargs['magic']


def get_map_version(header):
    version = header.version.enum_name
    if version == "xbox":
        if header.unknown != 0:
            version = "stubbs"
        elif header.build_date == map_build_dates["pcstubbs"]:
            version = "pcstubbs"
    return version


def get_map_header(map_data):
    header_def = map_header_def
    if map_data[704:708] == b'dehE' and map_data[1520:1524] == b'tofG':
        header_def = map_header_demo_def
    return header_def.build(rawdata=map_data)


def get_tag_index(map_data, header=None):
    map_data = decompress_map(map_data)
    if header is None:
        header = get_map_header(map_data)

    tag_index_def = tag_index_pc_def
    if header.version.data < 6 and get_map_version(header) != "pcstubbs":
        tag_index_def = tag_index_xbox_def

    tag_index = tag_index_def.build(
        rawdata=map_data, magic=get_map_magic(header),
        offset=header.tag_index_header_offset)

    return tag_index


def get_index_magic(header):
    return map_magics.get(get_map_version(header), 0)


def get_map_magic(header):
    return get_index_magic(header) - header.tag_index_header_offset


def decompress_map(comp_data, header=None):
    if header is None:
        header = get_map_header(comp_data)

    if header.version.data < 6:
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        if decomp_len > len(comp_data):
            decomp = zlib.decompress(comp_data[2048:])
            return comp_data[:2048] + decomp + b'X'*(decomp_len - len(decomp))

    # not actually compressed
    return comp_data


# Halo Demo maps have a different header
# structure with garbage filling the padding
map_header_demo = Struct("map header",
    Pad(2),
    LUEnum16("map type",
        "sp",
        "mp",
        "ui",
        ),
    Pad(700),
    LUEnum32('head', ('head', 'Ehed'), EDITABLE=False, DEFAULT='Ehed'),
    LSInt32("tag index meta len"),
    StrLatin1("build date", EDITABLE=False, SIZE=32),
    Pad(672),
    LSEnum32("version",
        ("xbox",   5),
        ("pcdemo", 6),
        ("pc", 7),
        ("ce", 609),
        ),
    ascii_str32("map name"),
    LSInt32("unknown"),
    LUInt32("crc32"),
    Pad(52),
    LSInt32("decomp len"),
    LSInt32("tag index header offset"),
    LUEnum32('foot', ('foot', 'Gfot'), EDITABLE=False, DEFAULT='Gfot'),
    Pad(524),
    SIZE=2048
    )

map_header = Struct("map header",
    LUEnum32('head', ('head', 'head'), EDITABLE=False, DEFAULT='head'),
    LSEnum32("version",
        ("xbox",   5),
        ("pcdemo", 6),
        ("pc", 7),
        ("ce", 609),
        ),
    LSInt32("decomp len"),
    LSInt32("unknown"),
    LSInt32("tag index header offset"),
    LSInt32("tag index meta len"),
    Pad(8),
    ascii_str32("map name"),
    StrLatin1("build date", EDITABLE=False, SIZE=32),
    LUEnum32("map type",
        "sp",
        "mp",
        "ui",
        ),
    LUInt32("crc32"),
    Pad(1940),
    LUEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    SIZE=2048
    )

'''
base_tag_magic, is somewhat interesting.
If you’ve ever gone through mapfiles with a hex editor, you
know about tag-swapping. You might go through a mapfile and
find a value like "E1880014"(in Blood Gulch, this is the
"scenery\rocks\boulder\shaders\boulder" tag. This number is
what we like to call a "Tag ID". Now if you are an experienced
modder at all, you know that you can swap a tag id with another
tag id of the same type (sometimes of different types) and you
can do some rather simple, but interesting things.

Well, the base_tag_magic is the number at which these tag id’s start.
For Blood Gulch, this number is "E1740000". This number varies
from map to map. You will notice an interesting property of the
tag id and the base tag occurs when you subtract one from the other:

Code:

E1880014 - E1740000 = 00140014

If you’ve used the "Offset List Export" feature of SparkEdit, you
will notice that this tag is the 0x15th element in the tag index.
If you were referencing the array in C, it would be TagIndex[0x14].
Pretty cool eh? Well, actually, in a few cases this property breaks down.
The upper 16 bits of that number do not always equal the lower 16 bits,
and the reason why is still a mystery. Some of us guess that it may be
some kind of "revision" number to keep track of assets, but we don’t
really know.
'''


tag_meta = Void("tag meta")

tag_data = Container("tag",
    CStrLatin1("tag path", POINTER=tag_path_pointer),
    tag_meta,
    )

tag_header = Struct("tag header",
    LUEnum32("class 1", GUI_NAME="primary tag class", INCLUDE=valid_tags),
    LUEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_tags),
    LUEnum32("class 3", GUI_NAME="tertiary tag class", INCLUDE=valid_tags),
    LUInt32("id"),
    LSInt32("path offset"),
    LSInt32("meta offset"),
    LUInt32("indexed"),
    # if indexed is 1, the meta_offset is the literal index in the
    # bitmaps, sounds, or loc cache that the meta data is located in.
    Pad(4),
    STEPTREE=tag_data,
    )

tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=tag_header,
    )

tag_index_xbox = Struct("tag index",
    LSInt32("tag index offset"),
    LUInt32("base tag magic"),
    LUInt32("map id"),
    LUInt32("tag count"),

    LUInt32("vertex object count"),
    LSInt32("model raw data offset"),

    LUInt32("indices object count"),
    LSInt32("indices offset"),
    LUInt32("tag sig", EDITABLE=False, DEFAULT='tags'),

    SIZE=36,
    STEPTREE=tag_index_array
    )

tag_index_pc = tipc = dict(tag_index_xbox)
tipc['ENTRIES'] += 1; tipc['SIZE'] += 4
tipc[9] = tipc[8]; tipc[8] = LUInt32("model raw data size")

map_header_def = BlockDef(map_header)
map_header_demo_def = BlockDef(map_header_demo)
tag_index_xbox_def = BlockDef(tag_index_xbox)
tag_index_pc_def = BlockDef(tag_index_pc)
