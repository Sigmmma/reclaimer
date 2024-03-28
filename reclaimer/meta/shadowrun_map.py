#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.halo1_map import  tag_path_pointer, tag_index_xbox,\
    tag_header as tag_index_header, tag_index_array_pointer
from reclaimer.shadowrun_prototype.common_descs import *

sr_tag_header = desc_variant(tag_index_header,
    UEnum32("class_1", GUI_NAME="primary tag class",   INCLUDE=sr_valid_tags),
    UEnum32("class_2", GUI_NAME="secondary tag class", INCLUDE=sr_valid_tags),
    UEnum32("class_3", GUI_NAME="tertiary tag class",  INCLUDE=sr_valid_tags),
    )
sr_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=sr_tag_header,
    POINTER=tag_index_array_pointer
    )
sr_tag_index = desc_variant(tag_index_xbox,
    STEPTREE=sr_tag_index_array
    )
sr_tag_index_def  = BlockDef(sr_tag_index)
