from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

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

def tag_path_pointer(parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    if new_value is None:
        return parent.path_offset - kwargs.get('magic', 0)
    parent.path_offset = new_value + kwargs.get('magic', 0)


def tag_index_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return parent.tag_index_offset - kwargs.get("magic", 0)
    parent.tag_index_offset = new_value + kwargs.get("magic", 0)


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
    UInt32("tag data size"),
    ascii_str32("build date", EDITABLE=False),
    Pad(672),
    UEnum32("version",
        ("halo1xbox",   5),
        ("halo1pcdemo", 6),
        ("halo1pc", 7),
        ("halo2", 8),
        ("halo3beta", 9),
        ("halo3", 11),
        ("halo1ce", 609),
        ),
    ascii_str32("map name"),
    UInt32("unknown"),
    UInt32("crc32"),
    Pad(52),
    UInt32("decomp len"),
    UInt32("tag index header offset"),
    UEnum32('foot', ('foot', 'Gfot'), EDITABLE=False, DEFAULT='Gfot'),
    Pad(524),
    SIZE=2048
    )

map_header = Struct("map header",
    UEnum32('head', ('head', 'head'), EDITABLE=False, DEFAULT='head'),
    UEnum32("version",
        ("halo1xbox",   5),
        ("halo1pcdemo", 6),
        ("halo1pc", 7),
        ("halo2", 8),
        ("halo3beta", 9),
        ("halo3", 11),
        ("halo1ce", 609),
        ),
    UInt32("decomp len"),
    UInt32("unknown"),
    UInt32("tag index header offset"),
    UInt32("tag data size"),
    Pad(8),
    ascii_str32("map name"),
    ascii_str32("build date", EDITABLE=False),
    UEnum16("map type",
        "sp",
        "mp",
        "ui",
        ),
    Pad(2),
    UInt32("crc32"),
    Pad(8),
    yelo_header,
    Pad(1940 - 8 - yelo_header[SIZE]),
    UEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    SIZE=2048
    )

tag_header = Struct("tag header",
    UEnum32("class 1", GUI_NAME="primary tag class", INCLUDE=valid_tags_os),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_tags_os),
    UEnum32("class 3", GUI_NAME="tertiary tag class", INCLUDE=valid_tags_os),
    UInt32("id"),
    UInt32("path offset"),
    UInt32("meta offset"),
    UInt32("indexed"),
    # if indexed is non-zero, the meta_offset is the literal index in
    # the bitmaps, sounds, or loc cache that the meta data is located in.
    # NOTE: indexed is NOT a bitfield, if it is non-zero it is True
    UInt32("pad"),
    STEPTREE=CStrLatin1("path", POINTER=tag_path_pointer),
    SIZE=32
    )

tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=tag_header, POINTER=tag_index_array_pointer
    )

tag_index_xbox = Struct("tag index",
    UInt32("tag index offset"),
    UInt32("scenario tag id"),
    UInt32("map id"),  # normally unused, but the scenario tag's header
    #                    can be used for spoofing the maps checksum
    UInt32("tag count"),

    UInt32("vertex parts count"),
    UInt32("model data offset"),

    UInt32("index parts count"),
    UInt32("index parts offset"),
    UInt32("tag sig", EDITABLE=False, DEFAULT='tags'),

    SIZE=36,
    STEPTREE=tag_index_array
    )

tag_index_pc = Struct("tag index",
    UInt32("tag index offset"),
    UInt32("scenario tag id"),
    UInt32("map id"),  # normally unused, but the scenario tag's header
    #                    can be used for spoofing the maps checksum
    UInt32("tag count"),

    UInt32("vertex parts count"),
    UInt32("model data offset"),

    UInt32("index parts count"),
    UInt32("vertex data size"),
    UInt32("model data size"),
    UInt32("tag sig", EDITABLE=False, DEFAULT='tags'),

    SIZE=40,
    STEPTREE=tag_index_array
    )

#tag_index_pc = tipc = dict(tag_index_xbox)
#tipc['ENTRIES'] += 1; tipc['SIZE'] += 4
#tipc[7] = UInt32("vertex data size")
#tipc[9] = tipc[8]; tipc[8] = UInt32("model data size")

map_header_def = BlockDef(map_header)
map_header_anni_def = BlockDef(map_header, endian=">")
map_header_demo_def = BlockDef(map_header_demo)

tag_index_xbox_def = BlockDef(tag_index_xbox)
tag_index_pc_def = BlockDef(tag_index_pc)
tag_index_anni_def = BlockDef(tag_index_pc, endian=">")
