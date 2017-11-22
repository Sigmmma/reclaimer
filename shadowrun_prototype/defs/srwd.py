from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return srwd_def

unknown_struct = Struct("unknown_struct",
    BytesRaw("unknown0", SIZE=1536),
    SIZE=1536
    )

srwd_def = TagDef("srwd",
    blam_header('srwd'),
    Struct('tagdata',
        BytesRaw("unknown0", SIZE=1280),
        reflexive("unknown1", unknown_struct),
        dependency("unknown2", "srwd"),
        BytesRaw("unknown3", SIZE=228),
        SIZE=1536
        ),

    ext=".shadowrun_weapon", endian=">"
    )
