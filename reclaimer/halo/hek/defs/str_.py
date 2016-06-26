from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

string_data_struct = rawdata_ref("string", StrLatin1)

str__body = Struct("tagdata",
    reflexive("strings", string_data_struct, 32767),
    SIZE=12,
    )


def get():
    return str__def

str__def = TagDef("str#",
    blam_header('str#'),
    str__body,

    ext=".string_list", endian=">"
    )
