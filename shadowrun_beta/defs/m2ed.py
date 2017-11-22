from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return m2ed_def

m2ed_def = TagDef("m2ed",
    blam_header('m2ed'),
    QStruct('tagdata',
        ),

    ext=".magic_2_effect_data", endian=">"
    )
