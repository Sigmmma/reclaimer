from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

child_ids = Struct("child id",
    BSInt32("entry reference"),
    SIZE=4
    )

referenced_by = Struct("referenced by", INCLUDE=child_ids)

entry = Struct("entry",
    rawdata_ref("name", StrUtf8, max_size=256),
    valid_tags_os,
    BSInt32("handle data"),
    BSInt32("flags"),
    reflexive("child ids", child_ids, 65536),
    reflexive("referenced by", referenced_by, 65536),
    SIZE=68
    )

tag__body = Struct("tagdata",
    reflexive("entries", entry, 65536),
    SIZE=36
    )

def get():
    return tag__def

tag__def = TagDef("tag+",
    blam_header_os('tag+'),
    tag__body,

    ext=".tag_database", endian=">"
    )
