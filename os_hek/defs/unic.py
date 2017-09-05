from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

string_reference = Struct("string reference",
    dependency_os("string id", "sidy"),
    SInt32("english offset"),
    SInt32("unused offset 1"),
    SInt32("unused offset 2"),
    SInt32("unused offset 3"),
    SInt32("unused offset 4"),
    SInt32("unused offset 5"),
    SInt32("unused offset 6"),
    SInt32("unused offset 7"),
    SInt32("unused offset 8"),
    SIZE=56
    )

unic_body = Struct("tagdata",
    reflexive("string references", string_reference,
        DYN_NAME_PATH='.string_id.filepath'),
    Pad(12),
    rawtext_ref("string data utf8", StrUtf8, max_size=18874368),

    SIZE=80
    )

def get():
    return unic_def

unic_def = TagDef("unic",
    blam_header_os('unic', 0),
    unic_body,

    ext=".multilingual_unicode_string_list", endian=">", tag_cls=HekTag
    )
