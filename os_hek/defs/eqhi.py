from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# I guess this is a tag that will be expanded upon later?

def get():
    return eqhi_def

eqhi_body = Struct("tagdata",
    SIZE=0
    )

eqhi_def = TagDef("eqhi",
    blam_header_os("eqhi", 0),
    eqhi_body,

    ext=".equipment_hud_interface", endian=">", tag_cls=HekTag
    )
