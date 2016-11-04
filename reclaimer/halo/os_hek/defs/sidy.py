from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

sidy_body = Struct("tagdata",
    rawdata_ref("documentation", StrAscii),
    SIZE=40
    )

def get():
    return sidy_def

sidy_def = TagDef("sidy",
    blam_header_os('sidy'),
    sidy_body,

    ext=".string_id_yelo", endian=">"
    )
