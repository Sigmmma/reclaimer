from ...hek.defs.jpt_ import *
from ..common_descs import *
from .objs.tag import StubbsTag

jpt__body = dict(jpt__body)
jpt__body[16] = dict(jpt__body[16])
jpt__body[17] = damage_modifiers

jpt__body[16][1] = SEnum16("category", *damage_category)
jpt__body[16][2] = Bool32("flags",
    "does not hurt owner",
    {NAME: "headshot", GUI_NAME: "causes headshots"},
    "pings resistant units",
    "does not hurt friends",
    "does not ping units",
    "detonates explosives",
    "only hurts shields",
    "causes flaming death",
    {NAME: "indicator_points_down", GUI_NAME: "damage indicators always point down"},
    "skips shields",
    "unknown1",
    {NAME: "multiplayer headshot", GUI_NAME: "causes multiplayer headshots"},
    "unknown2",
    )

    
def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header_stubbs('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">", tag_cls=StubbsTag
    )
