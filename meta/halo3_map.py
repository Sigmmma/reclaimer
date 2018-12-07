from ..h3.common_descs import *
from supyr_struct.defs.tag_def import TagDef, BlockDef


def compute_partition_offset(parent, **kwargs):
    if parent.size == 0:
        parent.file_offset = 0
        return

    partitions = parent.parent
    partition_num = partitions.index(parent)

    sections = partitions.parent.sections
    file_offset = 4096*3
    for i in range(2): # tag data is the third section
        file_offset += sections[i].size

    for i in range(partition_num):
        file_offset += partitions[i].size

    parent.file_offset = file_offset


def compute_section_offset(parent, **kwargs):
    if parent.size == 0:
        parent.file_offset = 0
        return

    sections = parent.parent
    section_num = sections.index(parent)

    file_offset = 4096*3
    for i in range(section_num):
        file_offset += sections[i].size

    parent.file_offset = file_offset


def virtual_ptr_to_file_ptr(ptr, section=0, map_header=None, **kwargs):
    if not map_header:
        return ptr
    elif section in (0, 1, 3):
        for section in map_header.sections:
            if ptr in range(section.virtual_address,
                            section.virtual_address + section.size):
                return ptr - section.virtual_address + section.file_offset
    else:
        for partition in map_header.partitions:
            if ptr in range(partition.load_address,
                            partition.load_address + partition.size):
                return ptr - partition.load_address + partition.file_offset
    raise ValueError("Pointer '%s' is not in any partitions." % ptr)


def file_ptr_to_virtual_ptr(ptr, section=0, map_header=None, **kwargs):
    if not map_header:
        return ptr
    elif section in (0, 1, 3):
        for section in map_header.sections:
            if ptr in range(section.file_offset,
                            section.file_offset + section.size):
                return ptr - section.file_offset + section.virtual_address
    else:
        for partition in map_header.partitions:
            if ptr in range(partition.file_offset,
                            partition.file_offset + partition.size):
                return ptr - partition.file_offset + partition.load_address
    raise ValueError("Pointer '%s' is not in any partitions." % ptr)


def string_id_table_name_pointer(parent=None, new_value=None, **kwargs):
    start = parent.parent.parent.string_id_table_file_offset
    if new_value is None:
        if parent.offset == -1:
            return start
        return parent.offset + start
    parent.offset = new_value - start

def tag_name_table_name_pointer(parent=None, new_value=None, **kwargs):
    start = parent.parent.parent.tag_name_table_file_offset
    if new_value is None:
        if parent.offset == -1:
            return start
        return parent.offset + start
    parent.offset = new_value - start


def compute_string_id_index_offset(parent, **kw):
    parent.string_id_index_file_offset = virtual_ptr_to_file_ptr(
        parent.get_root().string_id_index_offset,
        0, map_header=parent.get_root())

def compute_string_id_table_offset(parent, **kw):
    parent.string_id_table_file_offset = virtual_ptr_to_file_ptr(
        parent.get_root().string_id_table_offset,
        0, map_header=parent.get_root())

def compute_tag_name_index_offset(parent, **kw):
    parent.tag_name_index_file_offset = virtual_ptr_to_file_ptr(
        parent.get_root().tag_name_index_offset,
        0, map_header=parent.get_root())

def compute_tag_name_table_offset(parent, **kw):
    parent.tag_name_table_file_offset = virtual_ptr_to_file_ptr(
        parent.get_root().tag_name_table_offset,
        0, map_header=parent.get_root())


def tag_types_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return virtual_ptr_to_file_ptr(parent.tag_types_offset, 2, **kwargs)
    parent.tag_types_offset = file_ptr_to_virtual_ptr(new_value, **kwargs)

def tag_index_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return virtual_ptr_to_file_ptr(parent.tag_index_offset, 2, **kwargs)
    parent.tag_index_offset = file_ptr_to_virtual_ptr(new_value, **kwargs)

def root_tags_array_pointer(parent=None, new_value=None, **kwargs):
    if new_value is None:
        return virtual_ptr_to_file_ptr(parent.root_tags_offset, 2, **kwargs)
    parent.root_tags_offset = file_ptr_to_virtual_ptr(new_value, **kwargs)


string_id_table_entry = Container("string id table entry",
    SInt32("offset"),
    STEPTREE=CStrLatin1("string", POINTER=string_id_table_name_pointer),
    )

tag_name_table_entry = Container("tag name table entry",
    SInt32("offset"),
    STEPTREE=CStrLatin1("tag name", POINTER=tag_name_table_name_pointer),
    )


string_id_table = Array("string id table",
    SIZE="..string_id_count", SUB_STRUCT=string_id_table_entry,
    POINTER=".string_id_index_file_offset",
    )

tag_name_table = Array("tag name table",
    SIZE="..tag_name_count", SUB_STRUCT=tag_name_table_entry,
    POINTER=".tag_name_index_file_offset"
    )

partition = Struct("partition",
    UInt32("load address"),
    UInt32("size"),
    STEPTREE=Computed("file offset",
        COMPUTE_READ=compute_partition_offset, WIDGET_WIDTH=10 
        ),
    SIZE=8
    )

section = Struct("section",
    UInt32("virtual address"),
    UInt32("size"),
    Computed("file offset",
        COMPUTE_READ=compute_section_offset, WIDGET_WIDTH=10
        ),
    SIZE=8
    )

h3_map_header = Struct("map header",
    UEnum32('head', ('head', 'head'),
        EDITABLE=False, VISIBLE=False, DEFAULT='head'
        ),
    UEnum32("version",
        ("halo1xbox",   5),
        ("halo1pcdemo", 6),
        ("halo1pc", 7),
        ("halo2", 8),
        ("halo3beta", 9),
        ("halo3", 11),
        ("haloreach", 12),
        ("halo1ce", 609),
        ),
    UInt32("decomp len"),
    UInt32("unknown0", VISIBLE=False),
    UInt32("tag index header offset"),
    UInt32("tag buffer offset"),
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
    UInt16("unknown2", VISIBLE=False),
    UInt8("unknown3", VISIBLE=False),
    UInt8("unknown4", VISIBLE=False),
    UInt8("unknown5", VISIBLE=False),
    UInt8("unknown6", VISIBLE=False),
    Pad(20),
    UInt32("string id count"),
    UInt32("string id table size"),
    UInt32("string id index offset"),
    UInt32("string id table offset"),

    Bool8("required maps",
        "ui",
        "shared",
        "sp_shared"
        ),
    Pad(3),
    UInt32("build_date_low"),
    UInt32("build_date_high"),
    UInt32("unknown_ui_map_related_0"),
    UInt32("unknown_ui_map_related_1"),
    UInt32("unknown_shared_map_related_0"),
    UInt32("unknown_shared_map_related_1"),
    UInt32("unknown_sp_shared_map_related_0"),
    UInt32("unknown_sp_shared_map_related_1"),
    ascii_str32("map name"),
    Pad(4),
    StrLatin1("scenario tag path", SIZE=260),
    UInt32("tag name count"),
    UInt32("tag name table offset"),
    UInt32("tag name table size"),
    UInt32("tag name index offset"),

    UInt32("checksum"),
    BytesRaw("unknown9", SIZE=32, VISIBLE=False),
    UInt32("virtual address"),
    UInt32("xkd version"),
    Array("partitions", SUB_STRUCT=partition, SIZE=6),

    UInt32("unknown_count"),
    BytesRaw("unknown10", SIZE=12, VISIBLE=False),
    BytesRaw("unknown11", SIZE=316, VISIBLE=False),
    Array("offset masks", SUB_STRUCT=UInt32("mask"), SIZE=4,
        NAME_MAP={"debug": 0, "resource": 1, "tag": 2, "locale": 3}
        ),
    Array("sections", SUB_STRUCT=section, SIZE=4,
        NAME_MAP={"debug": 0, "resource": 1, "tag": 2, "locale": 3}
        ),

    Pad(11104),
    UEnum32('foot', ('foot', 'foot'), EDITABLE=False, DEFAULT='foot'),
    STEPTREE=Container("strings",
        Computed("string id index file offset",
            COMPUTE_READ=compute_string_id_index_offset, WIDGET_WIDTH=10
            ),
        Computed("string id table file offset",
            COMPUTE_READ=compute_string_id_table_offset, WIDGET_WIDTH=10
            ),
        Computed("tag name index file offset",
            COMPUTE_READ=compute_tag_name_index_offset, WIDGET_WIDTH=10
            ),
        Computed("tag name table file offset",
            COMPUTE_READ=compute_tag_name_table_offset, WIDGET_WIDTH=10
            ),
        string_id_table,
        tag_name_table,
        ),
    SIZE=4096*3, ENDIAN=">"
    )

h3_tag_type = Struct("tag type",
    UEnum32("class 1", GUI_NAME="primary tag class",   INCLUDE=valid_h3_tags),
    UEnum32("class 2", GUI_NAME="secondary tag class", INCLUDE=valid_h3_tags),
    UEnum32("class 3", GUI_NAME="tertiary tag class",  INCLUDE=valid_h3_tags),
    h3_string_id("string id"),  # specifies the string containing the file
    #                             extension for this class(i.e: bitm = bitmap)
    )

h3_tag_header = Struct("tag header",
    UInt16("tag type index"),
    UInt16("table index"),
    UInt32("offset"),
    SIZE=8
    )

h3_root_tag_ref = Struct("root tag ref",
    UEnum32("tag class", INCLUDE=valid_h3_tags),
    UInt32("id"),
    SIZE=8
    )

h3_tag_types_array = Array("tag types",
    SIZE=".tag_types_count", SUB_STRUCT=h3_tag_type,
    POINTER=tag_types_array_pointer
    )

h3_tag_index_array = TagIndex("tag index",
    SIZE=".tag_count", SUB_STRUCT=h3_tag_header,
    POINTER=tag_index_array_pointer
    )

h3_root_tags_array = TagIndex("root tags",
    SIZE=".root_tags_count", SUB_STRUCT=h3_root_tag_ref,
    POINTER=root_tags_array_pointer
    )

h3_tag_index = Container("tag index",
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

    h3_tag_types_array,
    h3_tag_index_array,
    h3_root_tags_array,
    ENDIAN=">"
    )

h3_map_header_def = BlockDef(h3_map_header)
h3_tag_index_def = BlockDef(h3_tag_index)
