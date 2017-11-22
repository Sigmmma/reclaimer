from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return m1ed_def

m1ed_def = TagDef("m1ed",
    blam_header('m1ed'),
    QStruct('tagdata',
        ),

    ext=".magic_1_effect_data", endian=">"
    )
