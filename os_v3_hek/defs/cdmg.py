from ...hek.defs.cdmg import *

damage = Struct("damage",
    SEnum16("priority",
        "none",
        "harmless",
        {NAME: "backstab", GUI_NAME: "lethal to the unsuspecting"},
        "emp",
        ),
    SEnum16("category", *damage_category),
    Bool32("flags",
        "does not hurt owner",
        {NAME: "headshot", GUI_NAME: "can cause headshots"},
        "pings resistant units",
        "does not hurt friends",
        "does not ping shields",
        "detonates explosives",
        "only hurts shields",
        "causes flaming death",
        {NAME: "indicator_points_down",
         GUI_NAME: "damage indicator always point down"},
        "skips shields",
        "only hurts one infection form",
        {NAME: "multiplayer headshot",
         GUI_NAME: "can cause multiplayer headshots"},
        "infection form pop",
        "YELO; 3D instantaneous acceleration"
        ),
    Pad(4),
    Float("damage lower bound"),
    QStruct("damage upper bound", INCLUDE=from_to),
    float_zero_to_one("vehicle passthrough penalty"),
    Pad(4),
    float_zero_to_one("stun"),
    float_zero_to_one("maximum stun"),
    float_sec("stun time"),
    Pad(4),
    QStruct("instantaneous acceleration",
        Float("i", UNIT_SCALE=per_sec_unit_scale),
        Float("j", UNIT_SCALE=per_sec_unit_scale),
        Float("k", UNIT_SCALE=per_sec_unit_scale),
        SIDETIP="[-inf,+inf]", ORIENT="h"
        ),
    )

cdmg_body = dict(cdmg_body)
cdmg_body[5] = damage

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
