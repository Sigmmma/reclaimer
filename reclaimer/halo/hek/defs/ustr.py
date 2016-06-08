from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

string_data_struct = rawdata_ref("string", FlStrUTF16)

ustr_body = Struct("tagdata",
    reflexive("strings", string_data_struct, 32767),
    SIZE=12,
    )


def get():
    return ustr_def

ustr_def = TagDef(
    blam_header('ustr'),
    ustr_body,
    
    NAME="unicode_string_list",
    
    ext=".unicode_string_list", def_id="ustr", endian=">"
    )
