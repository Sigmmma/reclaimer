from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef, BlockDef

def get(): return resource_tag_def


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

resource_tag_def = TagDef(resource_def.descriptor, endian="<", ext=".map")
