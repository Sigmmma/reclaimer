from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return srud_def

srud_def = TagDef("srud",
    blam_header('srud'),
    Struct('tagdata',
        BytesRaw("unknown", SIZE=5120),
        SIZE=5120
        ),

    ext=".shadowrun_unit", endian=">"
    )
