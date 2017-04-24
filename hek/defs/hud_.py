from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

hud__body = Struct("tagdata",
    dependency("digits bitmap", "bitm"),
    SInt8("bitmap digit width"),
    SInt8("screen digit width"),
    SInt8("x offset"),
    SInt8("y offset"),
    SInt8("decimal point width"),
    SInt8("colon width"),
    SIZE=100,
    )


def get():
    return hud__def

hud__def = TagDef("hud#",
    blam_header('hud#'),
    hud__body,

    ext=".hud_number", endian=">", tag_cls=HekTag
    )
