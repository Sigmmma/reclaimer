from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef, BlockDef

def get():
    return (full_resource_tag_def, resource_tag_def)


def tag_path_pointer(parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    t_head = parent.parent
    if new_value is None:
        return t_head.parent.parent.tag_paths_pointer + t_head.path_offset
    t_head.path_offset = new_value - t_head.parent.parent.tag_paths_pointer


tag_header = Struct("tag header",
    LUInt32("path offset"),
    LUInt32("size"),
    LUInt32("offset"),
    )

tag_path = Container("tag path",
    CStrLatin1("tag path"),
    )

resource_def = BlockDef("resource",
    LUEnum32("resource type",
        'NONE',
        'bitmaps',
        'sounds',
        'strings'
        ),
    LPointer32("tag paths pointer"),
    LPointer32("tag headers pointer"),
    LUInt32("tag count"),
    Array("tag paths",
        SIZE='.tag_count',
        SUB_STRUCT=tag_path, POINTER='.tag_paths_pointer',
        WIDGET=DynamicArrayFrame, DYN_NAME_PATH=".tag_path",
        ),
    Array("tag headers",
        SIZE='.tag_count', SUB_STRUCT=tag_header,
        POINTER='.tag_headers_pointer',
        ),
    endian="<"
    )

rsrc_tag = Container("tag",
    BytesRaw("data", SIZE="..size", POINTER="..offset"),
    CStrLatin1("path", POINTER=tag_path_pointer),
    )

full_tag_header = Struct("tag header",
    LUInt32("path offset"),
    LUInt32("size"),
    LUInt32("offset"),
    STEPTREE=rsrc_tag
    )

full_resource_def = BlockDef("full_resource",
    LUEnum32("resource type",
        'NONE',
        'bitmaps',
        'sounds',
        'strings'
        ),
    LPointer32("tag paths pointer"),
    LPointer32("tag headers pointer"),
    LUInt32("tag count"),
    Array("tags",
        SIZE='.tag_count', SUB_STRUCT=full_tag_header,
        POINTER='.tag_headers_pointer',
        ),
    endian="<"
    )

resource_tag_def = TagDef(resource_def.descriptor, endian="<", ext=".map")
full_resource_tag_def = TagDef(full_resource_def.descriptor, endian="<", ext=".map")
