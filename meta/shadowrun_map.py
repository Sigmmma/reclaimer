from .halo1_map import *
from ..shadowrun_prototype.common_descs import *


sr_tag_header = Struct("tag header",
    UEnum32("class 1", GUI_NAME="primary tag class",   INCLUDE=sr_valid_tags),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=sr_valid_tags),
    UEnum32("class 3", GUI_NAME="tertiary tag class",  INCLUDE=sr_valid_tags),
    tag_id_struct,
    UInt32("path offset"),
    UInt32("meta offset"),
    UInt32("indexed"),
    # if indexed is 1, the meta_offset is the literal index in the
    # bitmaps, sounds, or loc cache that the meta data is located in.
    Pad(4),
    STEPTREE=tag_data, SIZE=32
    )

sr_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=sr_tag_header,
    POINTER=tag_index_array_pointer
    )

sr_tag_index = Struct("tag index",
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
    STEPTREE=sr_tag_index_array
    )

sr_tag_index_def  = BlockDef(sr_tag_index)
