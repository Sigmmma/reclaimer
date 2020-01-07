#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.halo1_map import tag_path_pointer, tag_index_array_pointer
from reclaimer.stubbs.common_descs import *


stubbs_tag_header = Struct("tag header",
    UEnum32("class 1", GUI_NAME="primary tag class",   INCLUDE=stubbs_valid_tags),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=stubbs_valid_tags),
    UEnum32("class 3", GUI_NAME="tertiary tag class",  INCLUDE=stubbs_valid_tags),
    UInt32("id"),
    UInt32("path offset"),
    UInt32("meta offset"),
    UInt32("indexed"),
    # if indexed is 1, the meta_offset is the literal index in the
    # bitmaps, sounds, or loc cache that the meta data is located in.
    Pad(4),
    STEPTREE=CStrTagRef("path", POINTER=tag_path_pointer, MAX=768),
    SIZE=32
    )

stubbs_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=stubbs_tag_header,
    POINTER=tag_index_array_pointer
    )

stubbs_tag_index = Struct("tag index",
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
    STEPTREE=stubbs_tag_index_array
    )

stubbs_tag_index_def  = BlockDef(stubbs_tag_index)
