from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return srwd_def

srwd_def = TagDef("srwd",
    blam_header('srwd'),
    QStruct('tagdata',
        ),

    ext=".shadowrun_weapon_data", endian=">"
    )
