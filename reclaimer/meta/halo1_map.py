#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

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

from reclaimer.common_descs import *

from supyr_struct.defs.block_def import BlockDef
from supyr_struct.util import desc_variant

def tag_path_pointer(parent=None, new_value=None, magic=0, **kwargs):
    '''
    Calculates the pointer value for a tag_path based on the file offset.
    '''
    if parent is None:
        raise KeyError()
    if new_value is None:
        return parent.path_offset - magic
    parent.path_offset = new_value + magic


def tag_index_array_pointer(parent=None, new_value=None, magic=0, **kwargs):
    '''
    Calculates the pointer value for a tag_index array based on file offset.
    '''
    if new_value is None:
        return parent.tag_index_offset - magic
    parent.tag_index_offset = new_value + magic


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

vap_block = Struct("vap_block",
    # File offset of the compressed block
    UInt32("file_offset"),

    # File size of the compressed block
    UInt32("file_size"),

    # Decompressed size of the compressed block
    UInt32("decompressed_size"),

    # Reserved for potential future usage
    UInt32("reserved"),
    )

# validated archive pattern(uh huh, sure)
vap_header = Struct("vap_header",
    # File size of the map when decompressed, include header size
    UInt32("decompressed_size"),
    UEnum16("compression_type",
        "uncompressed",
        "lzma",
    ),
    UEnum16("vap_version",
        "chimera_1",
        "next",
    ),

    # Number of blocks. If 0, data is assumed to be one contiguous stream
    UInt32("block_count"),
    # File size of the map when compressed, include header size
    UInt32("compressed_size"),

    UEnum32("feature_level",
        "chimera_1",
        "next",
    ),

    # Player limit (campaign). Set to 0 for multiplayer and user interface maps
    UInt16("max_players"),
    # Reserved for future use. Leave it at 0
    Pad(10),

    # Build date of the map in ISO 8601 (yyyy-mm-ddThh:mm:ss.fffffffff) format
    ascii_str32("build_date"),

    # Human-readable of the map
    ascii_str32("name"),

    # Human-readable description of the map
    StrLatin1("description", SIZE=128),
    Pad(256),
    STEPTREE=Array("blocks",
        SIZE=".block_count", SUB_STRUCT=vap_block
        ),
    SIZE=480
    )

# Halo Demo maps have a different header
# structure with garbage filling the padding
map_header_demo = Struct("map header",
    Pad(2),
    gen1_map_type, # NOTE: in common_descs.py
    Pad(700),
    UEnum32('head', ('head', 'Ehed'), EDITABLE=False, DEFAULT='Ehed'),
    UInt32("tag data size"),
    ascii_str32("build date", EDITABLE=False),
    Pad(672),
    map_version, # NOTE: in common_descs.py
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
    UEnum32('head', ('head', 'head'), DEFAULT='head'),
    map_version, # NOTE: in common_descs.py
    UInt32("decomp len"),
    UInt32("unknown"),
    UInt32("tag index header offset"),
    UInt32("tag data size"),
    Pad(8),
    ascii_str32("map name"),
    ascii_str32("build date", EDITABLE=False),
    gen1_map_type, # NOTE: in common_descs.py
    Pad(2),
    UInt32("crc32"),
    Pad(1),
    Pad(3),
    Pad(4),
    yelo_header,
    UEnum32('foot', ('foot', 'foot'), DEFAULT='foot', OFFSET=2044),
    SIZE=2048
    )

mcc_flags = Bool8("mcc_flags", 
    "use_bitmaps_map",
    "use_sounds_map",
    "disable_remastered_sync",
    )

map_header_mcc = desc_variant(
    map_header,
    ("pad_12", mcc_flags),
    )

map_header_vap = desc_variant(
    map_header,
    ("yelo_header", Struct("vap_header", INCLUDE=vap_header, OFFSET=128)),
    verify=False,
    )

tag_header = Struct("tag_header",
    UEnum32("class_1", GUI_NAME="primary tag class", INCLUDE=valid_tags_os),
    UEnum32("class_2", GUI_NAME="secondary tag class", INCLUDE=valid_tags_os),
    UEnum32("class_3", GUI_NAME="tertiary tag class", INCLUDE=valid_tags_os),
    UInt32("id"),
    UInt32("path_offset"),
    UInt32("meta_offset"),
    UInt8("indexed"),
    Pad(3),
    # if indexed is non-zero, the meta_offset is the literal index in
    # the bitmaps, sounds, or loc cache that the meta data is located in.
    # NOTE: indexed is NOT a bitfield, if it is non-zero it is True
    UInt32("pad"),
    STEPTREE=CStrTagRef("path", POINTER=tag_path_pointer, MAX=768),
    SIZE=32
    )

tag_index_array = TagIndex("tag_index",
    SIZE=".tag_count", SUB_STRUCT=tag_header, POINTER=tag_index_array_pointer
    )

tag_index_pc = Struct("tag_index",
    UInt32("tag_index_offset"),
    UInt32("scenario_tag_id"),
    UInt32("map_id"),  # normally unused, but can be used
                       # for spoofing the maps checksum.
    UInt32("tag_count"),

    UInt32("vertex_parts_count"),
    UInt32("model_data_offset"),

    UInt32("index_parts_count"),
    UInt32("index_parts_offset"),
    UInt32("model_data_size"),
    UInt32("tag_sig", EDITABLE=False, DEFAULT='tags'),

    SIZE=40,
    STEPTREE=tag_index_array
    )

tag_index_xbox = desc_variant(tag_index_pc,
    ("model_data_size", Pad(0)),
    SIZE=36, verify=False
    )

map_header_def = BlockDef(map_header)
map_header_anni_def = BlockDef(map_header, endian=">")
map_header_demo_def = BlockDef(map_header_demo)
map_header_vap_def = BlockDef(map_header_vap)

tag_index_xbox_def = BlockDef(tag_index_xbox)
tag_index_pc_def = BlockDef(tag_index_pc)
tag_index_anni_def = BlockDef(tag_index_pc, endian=">")

map_header_vap_def = BlockDef(map_header_vap)
map_header_mcc_def = BlockDef(map_header_mcc)
