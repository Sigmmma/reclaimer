import zlib
import os

from ..h3.common_descs import *
from supyr_struct.defs.tag_def import TagDef


def tag_name_table_name_pointer(parent=None, new_value=None, **kwargs):
    header = parent.parent.parent.parent
    if new_value is None:
        if parent.offset == -1:
            return header.tag_name_table_offset - HALO3_HEADER_MAGIC
        return parent.offset + (header.tag_name_table_offset -
                                HALO3_HEADER_MAGIC)
    parent.offset = new_value - (header.tag_name_table_offset -
                                 HALO3_HEADER_MAGIC)


def string_id_table_name_pointer(parent=None, new_value=None, **kwargs):
    header = parent.parent.parent.parent
    if new_value is None:
        if parent.offset == -1:
            return header.string_id_table_offset - HALO3_HEADER_MAGIC
        return parent.offset + (header.string_id_table_offset -
                                HALO3_HEADER_MAGIC)
    parent.offset = new_value - (header.string_id_table_offset -
                                 HALO3_HEADER_MAGIC)


def tag_name_index_pointer(parent=None, new_value=None, **kwargs):
    header = parent.parent
    if new_value is None:
        return header.tag_name_index_offset - HALO3_HEADER_MAGIC
    header.tag_name_index_offset = new_value + HALO3_HEADER_MAGIC


def string_id_index_pointer(parent=None, new_value=None, **kwargs):
    header = parent.parent
    if new_value is None:
        return header.string_id_index_offset - HALO3_HEADER_MAGIC
    header.string_id_index_offset = new_value + HALO3_HEADER_MAGIC


def tag_types_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return parent.tag_types_offset - kwargs.get("magic", 0)
    parent.tag_types_offset = new_value + kwargs.get("magic", 0)


def tag_index_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return parent.tag_index_offset - kwargs.get("magic", 0)
    parent.tag_index_offset = new_value + kwargs.get("magic", 0)


def root_tags_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return parent.root_tags_offset - kwargs.get("magic", 0)
    parent.root_tags_offset = new_value + kwargs.get("magic", 0)


string_id_table_entry = Container("string id table entry",
    SInt32("offset"),
    STEPTREE=CStrLatin1("string id", POINTER=string_id_table_name_pointer),
    )

tag_name_table_entry = Container("tag name table entry",
    SInt32("offset"),
    STEPTREE=CStrLatin1("tag name", POINTER=tag_name_table_name_pointer),
    )


string_id_table = Array("string id table",
    SIZE="..string_id_count", SUB_STRUCT=string_id_table_entry,
    POINTER=string_id_index_pointer
    )

tag_name_table = Array("tag name table",
    SIZE="..tag_name_count", SUB_STRUCT=tag_name_table_entry,
    POINTER=tag_name_index_pointer
    )

halo3_map_header = Struct("map header",
    UEnum32('head', ('head', 'head'), EDITABLE=False, DEFAULT='head'),
    UEnum32("version",
        ("halo1xbox",   5),
        ("halo1pcdemo", 6),
        ("halo1pc", 7),
        ("halo2", 8),
        ("halo3", 11),
        ("halo1ce", 609),
        ),
    UInt32("decomp len"),
    UInt32("unknown0"),
    UInt32("tag index header offset"),  # uses magic
    UInt32("tag buffer offset"),  # uses header magic
    UInt32("virtual size"),
    Pad(256),

    ascii_str32("build date"),
    UEnum16("map type",
        "sp",
        "mp",
        "ui",
        "shared",
        "sharedsp",
        ),
    UEnum16("unknown2"),
    UEnum8("unknown3"),
    UEnum8("unknown4"),
    UEnum8("unknown5"),
    UEnum8("unknown6"),
    Pad(20),
    UInt32("string id count"),
    UInt32("string id table size"),
    UInt32("string id index offset"),  # uses header magic
    UInt32("string id table offset"),  # uses header magic
    Pad(4),
    UInt32("unknown7"),
    UInt32("unknown8"),  # uses magic?
    Pad(24),
    ascii_str32("map name"),
    Pad(4),
    StrLatin1("scenario tag path", SIZE=260),
    UInt32("tag name count"),
    UInt32("tag name table offset"),  # uses header magic
    UInt32("tag name table size"),
    UInt32("tag name index offset"),  # uses header magic

    BytesRaw("unknown9", SIZE=36),
    UInt32("virtual base address"),
    UInt32("xkd version"),
    Array("partitions",
        SUB_STRUCT=QStruct("partition",
            UInt32("load address"),
            UInt32("size"),
            SIZE=8
            ),
        SIZE=6
        ),

    BytesRaw("unknown10", SIZE=332),
    Array("offset masks",
        SUB_STRUCT=UInt32("mask"),
        SIZE=4
        ),
    Array("sections",
        SUB_STRUCT=QStruct("section",
            UInt32("virtual address"),
            UInt32("size"),
            SIZE=8
            ),
        SIZE=4
        ),

    Pad(11104),
    UEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    SIZE=4096*3,
    STEPTREE=Container("strings",
        string_id_table,
        tag_name_table,
        )
    )

halo3_tag_type = Struct("tag header",
    UEnum32("class 1", GUI_NAME="primary tag class",   INCLUDE=valid_h3_tags),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_h3_tags),
    UEnum32("class 3", GUI_NAME="tertiary tag class",  INCLUDE=valid_h3_tags),
    UInt32("string id"),
    )

halo3_tag_header = Struct("tag header",
    UInt16("tag type index"),
    UInt16("table index"),
    UInt32("offset"),
    SIZE=8
    )

halo3_root_tag_ref = Struct("root tag ref",
    UEnum32("tag class", INCLUDE=valid_h3_tags),
    h3_tag_id_struct,
    SIZE=8
    )

halo3_tag_types_array = Array("tag types",
    SIZE=".tag_types_count", SUB_STRUCT=halo3_tag_type,
    POINTER=tag_types_array_pointer
    )

halo3_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=halo3_tag_header,
    POINTER=tag_index_array_pointer
    )

halo3_root_tags_array = TagIndex("root tags",
    SIZE=".root_tags_count", SUB_STRUCT=halo3_root_tag_ref,
    POINTER=root_tags_array_pointer
    )

halo3_tag_index = Container("tag index",
    UInt32("tag types count"),
    UInt32("tag types offset"),

    UInt32("tag count"),
    UInt32("tag index offset"),

    UInt32("root tags count"),
    UInt32("root tags offset"),
    UInt32("unknown count"),
    UInt32("unknown offset"),

    UInt32("crc32"),
    UInt32("tag sig", EDITABLE=False, DEFAULT='tags'),

    halo3_tag_types_array,
    halo3_tag_index_array,
    halo3_root_tags_array
    )

halo3_map_header_def = BlockDef(halo3_map_header, endian=">")
halo3_tag_index_def = BlockDef(halo3_tag_index, endian=">")
