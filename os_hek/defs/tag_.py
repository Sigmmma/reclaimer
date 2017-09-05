from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

child_ids = Struct("child id",
    dyn_senum32("entry reference",
        DYN_NAME_PATH="tagdata.entries.STEPTREE[DYN_I].name.data"),
    SIZE=4
    )

referenced_by = Struct("referenced by", INCLUDE=child_ids)

entry = Struct("entry",
    rawtext_ref("name", StrUtf8, max_size=256, widget=EntryFrame),
    UEnum32("group tag", INCLUDE=valid_tags_os, GUI_NAME="group tag"),
    SInt32("handle data"),
    SInt32("flags"),
    reflexive("child ids", child_ids, 65536),
    reflexive("referenced by", referenced_by, 65536),
    SIZE=68
    )

tag__body = Struct("tagdata",
    reflexive("entries", entry, 65536, DYN_NAME_PATH='.name.data'),
    SIZE=36
    )

def get():
    return tag__def

tag__def = TagDef("tag+",
    blam_header_os('tag+'),
    tag__body,

    ext=".tag_database", endian=">", tag_cls=HekTag
    )
