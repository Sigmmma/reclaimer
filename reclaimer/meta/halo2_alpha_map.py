#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.h2.common_descs import *
from reclaimer.meta.halo2_map import valid_h2_tags
from reclaimer.meta.halo1_map import tag_path_pointer, tag_index_array_pointer


h2_alpha_map_header = Struct("map header",
    UEnum32('head', ('head', 'head'), EDITABLE=False, DEFAULT='head'),
    UEnum32("version",
        ("halo2alpha", 7),
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
        "shared",
        ),
    Pad(2),
    UInt32("crc32"),
    UInt32("unknown0"),
    Pad(8),
    UInt32("unknown1"),  # seems to be a count?
    UInt32("crazy data offset"),
    UInt32("crazy data len"),
    UInt32("string id padded offset"),
    UInt32("string id count"),
    UInt32("string id table size"),
    UInt32("string id index offset"),
    UInt32("string id table offset"),
    BytesRaw("unknown_bytes", SIZE=16),

    Pad(1880),
    UEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    SIZE=2048
    )

tag_header = Struct("tag header",
    UEnum32("class 1", GUI_NAME="primary tag class", INCLUDE=valid_h2_tags),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_h2_tags),
    UEnum32("class 3", GUI_NAME="tertiary tag class", INCLUDE=valid_h2_tags),
    UInt32("id"),
    UInt32("path offset"),
    UInt32("meta offset"),
    Bool32("flags", *("flag_%s" % i for i in range(32))),  # this is a guess
    UInt32("pad"),
    STEPTREE=CStrLatin1("path", POINTER=tag_path_pointer),
    SIZE=32
    )

tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=tag_header, POINTER=tag_index_array_pointer
    )

h2_alpha_tag_index = Struct("tag index",
    UInt32("tag index offset"),
    UInt32("scenario tag id"),
    UInt32("unknown"),
    UInt32("tag count"),
    UInt32("tag sig", EDITABLE=False, DEFAULT='tags'),

    SIZE=20,
    STEPTREE=tag_index_array
    )

h2_alpha_map_header_def = BlockDef(h2_alpha_map_header)
h2_alpha_tag_index_def = BlockDef(h2_alpha_tag_index)
