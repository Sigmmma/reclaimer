from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return t1ed_def

t1ed_def = TagDef("t1ed",
    blam_header('t1ed'),
    Struct('tagdata',
        ),

    ext=".tech_1_effect_data", endian=">"
    )
