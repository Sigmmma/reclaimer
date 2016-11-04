from .obje import *
from .item import *
from supyr_struct.defs.tag_def import TagDef

garb_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    SIZE=944,
    )


def get():
    return garb_def

garb_def = TagDef("garb",
    blam_header('garb'),
    garb_body,

    ext=".garbage", endian=">"
    )
