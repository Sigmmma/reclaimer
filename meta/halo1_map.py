import zlib
import os

from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.buffer import PeekableMmap
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
    if new_value is None:
        return t_head.path_offset - kwargs['magic']

    t_head.path_offset = new_value + kwargs['magic']


def tag_index_array_pointer(node=None, parent=None, new_value=None, **kwargs):
    if new_value is None:
        return parent.tag_index_offset - kwargs.get("magic")
    parent.tag_index_offset = new_value + kwargs.get("magic")


def get_map_version(header):
    version = header.version.enum_name
    if version == "xbox":
        if header.build_date == map_build_dates["stubbs"]:
            version = "stubbs"
        elif header.build_date == map_build_dates["pcstubbs"]:
            version = "pcstubbs"
    elif hasattr(header, "yelo_header") and (
        header.yelo_header.yelo.enum_name == "yelo"):
        return "yelo"
    return version


def get_map_header(map_data):
    header_def = map_header_def
    if map_data[704:708] == b'dehE' and map_data[1520:1524] == b'tofG':
        header_def = map_header_demo_def
    return header_def.build(rawdata=map_data)


def get_tag_index(map_data, header=None):
    if header is None:
        header = get_map_header(map_data)

    map_data = decompress_map(map_data, header)

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


def is_compressed(comp_data, header):
    if header.version.data < 6:
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        return decomp_len > len(comp_data)
    return False


def decompress_map(comp_data, header=None, decomp_path=None):
    if header is None:
        header = get_map_header(comp_data)

    if is_compressed(comp_data, header):
        comp_data.seek(0)
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        if decomp_path is None:
            decomp_path = "decomp.map"
        else:
            temp_dir = os.path.dirname(decomp_path)
            if not os.path.isdir(temp_dir):
                os.makedirs(temp_dir)

        print("Decompressing map to: %s" % decomp_path)
        with open(decomp_path, "wb+") as f:
            f.write(comp_data[:2048])
            comp_data = comp_data[2048:]
            decomp_obj = zlib.decompressobj()

            while comp_data:
                # decompress map 64Mb at a time
                f.write(decomp_obj.decompress(comp_data, 64*1024*1024))
                comp_data = decomp_obj.unconsumed_tail

            # pad the file to its decompressed length
            f.write(b'\xca'*(decomp_len - f.tell()))

        # have to do this separate or seeking will be fucked
        with open(decomp_path, "rb+") as f:
            decomp_data = PeekableMmap(f.fileno(), 0)
    else:
        decomp_data = comp_data

    # not actually compressed
    return decomp_data


yelo_header = Struct("yelo header",
    UEnum32("yelo", ('yelo', 'yelo'), EDITABLE=False, DEFAULT='yelo'),
    UEnum16("version type",
        ("version", 1),
        ("version minimum build", 2)
        ),
    Bool16("flags",
        "uses memory upgrades",
        "uses mod data files",
        "is protected",
        "uses game state upgrades",
        "has compression params",
        ),
    QStruct("tag versioning",
        UInt8("project yellow"),
        UInt8("project yellow globals"),
        Pad(2),
        SIZE=4
        ),

    Float("memory upgrade multiplier"),

    Struct("cheape definitions",
        UInt32("size"),
        UInt32("decompressed size"),
        UInt32("offset"),
        Pad(4),

        ascii_str32("build string"),
        SIZE=48
        ),

    ascii_str32("mod name"),

    Struct("build info",
        Pad(2),
        UEnum16("stage",
            "ship",
            "alpha",
            "beta",
            "delta",
            "epsilon",
            "release",
            ),
        UInt32("revision"),
        Timestamp64("timestamp"),

        ascii_str32("build string"),

        QStruct("cheape",
            UInt8("maj"),
            UInt8("min"),
            UInt16("build"),
            ),
        BytesRaw("uuid buffer", SIZE=16),

        QStruct("minimum os build",
            UInt8("maj"),
            UInt8("min"),
            UInt16("build"),
            ),
        Pad(4*3),
        SIZE=84
        ),

    QStruct("resources",
        UInt32("compression params header offset"),
        UInt32("tag symbol storage header offset"),
        UInt32("string id storage header offset"),
        UInt32("tag string to id storage header offset"),
        SIZE=16
        ),

    SIZE=196
    )


# Halo Demo maps have a different header
# structure with garbage filling the padding
map_header_demo = Struct("map header",
    Pad(2),
    UEnum16("map type",
        "sp",
        "mp",
        "ui",
        ),
    Pad(700),
    UEnum32('head', ('head', 'Ehed'), EDITABLE=False, DEFAULT='Ehed'),
    SInt32("tag index meta len"),
    StrLatin1("build date", EDITABLE=False, SIZE=32),
    Pad(672),
    SEnum32("version",
        ("xbox",   5),
        ("pcdemo", 6),
        ("pc", 7),
        ("ce", 609),
        ),
    ascii_str32("map name"),
    SInt32("unknown"),
    UInt32("crc32"),
    Pad(52),
    SInt32("decomp len"),
    SInt32("tag index header offset"),
    UEnum32('foot', ('foot', 'Gfot'), EDITABLE=False, DEFAULT='Gfot'),
    Pad(524),
    SIZE=2048
    )

map_header = Struct("map header",
    UEnum32('head', ('head', 'head'), EDITABLE=False, DEFAULT='head'),
    SEnum32("version",
        ("xbox",   5),
        ("pcdemo", 6),
        ("pc", 7),
        ("ce", 609),
        ),
    SInt32("decomp len"),
    SInt32("unknown"),
    SInt32("tag index header offset"),
    SInt32("tag index meta len"),
    Pad(8),
    ascii_str32("map name"),
    StrLatin1("build date", EDITABLE=False, SIZE=32),
    UEnum32("map type",
        "sp",
        "mp",
        "ui",
        ),
    UInt32("crc32"),
    Pad(8),
    yelo_header,
    Pad(1940 - 8 - yelo_header[SIZE]),
    UEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    SIZE=2048
    )

'''
main_scenario_tag_id, is somewhat interesting.
If you’ve ever gone through mapfiles with a hex editor, you
know about tag-swapping. You might go through a mapfile and
find a value like "E1880014"(in Blood Gulch, this is the
"scenery\rocks\boulder\shaders\boulder" tag. This number is
what we like to call a "Tag ID". Now if you are an experienced
modder at all, you know that you can swap a tag id with another
tag id of the same type (sometimes of different types) and you
can do some rather simple, but interesting things.

Well, the main_scenario_tag_id is the number at which these tag id’s start.
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
    UEnum32("class 1", GUI_NAME="primary tag class", INCLUDE=valid_tags_os),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_tags_os),
    UEnum32("class 3", GUI_NAME="tertiary tag class", INCLUDE=valid_tags_os),
    tag_id_struct,
    UInt32("path offset"),
    UInt32("meta offset"),
    UInt32("indexed"),
    # if indexed is 1, the meta_offset is the literal index in the
    # bitmaps, sounds, or loc cache that the meta data is located in.
    Pad(4),
    STEPTREE=tag_data, SIZE=32
    )

tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=tag_header, POINTER=tag_index_array_pointer
    )

tag_index_xbox = Struct("tag index",
    UInt32("tag index offset"),
    QStruct("scenario tag id", INCLUDE=tag_id_struct),
    UInt32("map id"),
    UInt32("tag count"),

    UInt32("vertex parts count"),
    UInt32("model data offset"),

    UInt32("index parts count"),
    UInt32("index parts offset"),
    UInt32("tag sig", EDITABLE=False, DEFAULT='tags'),

    SIZE=36,
    STEPTREE=tag_index_array
    )

tag_index_pc = tipc = dict(tag_index_xbox)
tipc['ENTRIES'] += 1; tipc['SIZE'] += 4
tipc[7] = LUInt32("vertex data size")
tipc[9] = tipc[8]; tipc[8] = LUInt32("index data size")

map_header_def = BlockDef(map_header)
map_header_demo_def = BlockDef(map_header_demo)
tag_index_xbox_def = BlockDef(tag_index_xbox)
tag_index_pc_def = BlockDef(tag_index_pc)
