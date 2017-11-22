from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return srud_def

srud_def = TagDef("srud",
    blam_header('srud'),
    QStruct('tagdata',
        ),

    ext=".shadowrun_unit_data", endian=">"
    )
