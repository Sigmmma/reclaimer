#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.halo1_map import tag_index_xbox, map_version,\
    tag_header as tag_index_header, tag_path_pointer, tag_index_array_pointer
from reclaimer.stubbs.common_descs import *

stubbs_tag_index_header = desc_variant(tag_index_header,
    UEnum32("class_1", GUI_NAME="primary tag class",   INCLUDE=stubbs_valid_tags),
    UEnum32("class_2", GUI_NAME="secondary tag class", INCLUDE=stubbs_valid_tags),
    UEnum32("class_3", GUI_NAME="tertiary tag class",  INCLUDE=stubbs_valid_tags),
    )

stubbs_64bit_tag_index_header = desc_variant(stubbs_tag_index_header,
    Pointer64("path_offset"),
    Pointer64("meta_offset"),
    verify=False,
    SIZE=40
    )

stubbs_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=stubbs_tag_index_header,
    POINTER=tag_index_array_pointer
    )

stubbs_64bit_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=stubbs_64bit_tag_index_header,
    POINTER=tag_index_array_pointer
    )

stubbs_tag_index = desc_variant(tag_index_xbox,
    STEPTREE=stubbs_tag_index_array
    )

stubbs_64bit_tag_index = Struct("tag_index",
    Pointer64("tag_index_offset"),
    UInt32("scenario_tag_id"),
    UInt32("map_id"),  # normally unused, but can be used
                       # for spoofing the maps checksum.
    UInt32("tag_count"),

    UInt32("vertex_parts_count"),
    Pointer64("model_data_offset"),

    UInt32("index_parts_count"),
    Pad(4),
    Pointer64("index_parts_offset"),
    UInt32("model_data_size"),
    UInt32("tag_sig", EDITABLE=False, DEFAULT='tags'),
    STEPTREE=stubbs_64bit_tag_index_array,
    SIZE=56
    )

stubbs_tag_index_def        = BlockDef(stubbs_tag_index)
stubbs_64bit_tag_index_def  = BlockDef(stubbs_64bit_tag_index)
