from ...hek.defs.cdmg import *
from ..common_descs import *

cdmg_body = dict(cdmg_body)
cdmg_body[5] = dict(cdmg_body[5])
cdmg_body[6] = damage_modifiers
cdmg_body[5][1] = SEnum16("category", *damage_category)
cdmg_body[5][2] = Bool32("flags",
    "does not hurt owner",
    {NAME: "headshot", GUI_NAME: "can cause headshots"},
    "pings resistant units",
    "does not hurt friends",
    "does not ping shields",
    "detonates explosives",
    "only hurts shields",
    "causes flaming death",
    {NAME: "indicator_points_down", GUI_NAME: "damage indicator always point down"},
    "skips shields",
    "unknown1",
    {NAME: "multiplayer headshot", GUI_NAME: "causes multiplayer headshots"},
    "unknown2",
    )
    
def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header_stubbs('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">"
    )
