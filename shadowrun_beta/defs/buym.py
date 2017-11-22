from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return buym_def

buym_def = TagDef("buym",
    blam_header('buym'),
    QStruct('tagdata',
        ),

    ext=".buy_menu", endian=">"
    )
