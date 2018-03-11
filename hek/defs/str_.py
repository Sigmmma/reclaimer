from ...common_descs import *
from .objs.str_ import Str_Tag
from supyr_struct.defs.tag_def import TagDef

string_data_struct = rawtext_ref("string", StrLatin1, max_size=4096)

str__body = Struct("tagdata",
    reflexive("strings", string_data_struct, 32767, widget=TextFrame,
        DYN_NAME_PATH='.data'),
    SIZE=12,
    )


def get():
    return str__def

str__def = TagDef("str#",
    blam_header('str#'),
    str__body,

    ext=".string_list", endian=">", tag_cls=Str_Tag
    )
