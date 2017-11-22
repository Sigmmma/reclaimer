from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return srac_def

srac_def = TagDef("srac",
    blam_header('srac'),
    QStruct('tagdata',
        ),

    ext=".shadowrun_actor", endian=">"
    )
