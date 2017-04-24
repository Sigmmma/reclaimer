from ...hek.defs.jpt_ import *

damage = Struct("damage",
    BSEnum16("priority",
        "none",
        "harmless",
        {NAME: "backstab", GUI_NAME: "lethal to the unsuspecting"},
        "emp",
        ),
    BSEnum16("category", *damage_category),
    BBool32("flags",
        "does not hurt owner",
        {NAME: "headshot", GUI_NAME: "causes headshots"},
        "pings resistant units",
        "does not hurt friends",
        "does not ping units",
        "detonates explosives",
        "only hurts shields",
        "causes flaming death",
        {NAME: "indicator_points_down",
         GUI_NAME: "damage indicators always point down"},
        "skips shields",
        "only hurts one infection form",
        {NAME: "multiplayer headshot",
         GUI_NAME: "causes multiplayer headshots"},
        "infection form pop",
        "YELO; 3D instantaneous acceleration"
        ),
    float_wu("aoe core radius"),
    BFloat("damage lower bound"),
    QStruct("damage upper bound", INCLUDE=from_to),
    float_zero_to_one("vehicle passthrough penalty"),
    float_zero_to_one("active camouflage damage"),
    float_zero_to_one("stun"),
    float_zero_to_one("maximum stun"),
    float_sec("stun time"),
    Pad(4),
    QStruct("instantaneous acceleration",
        BFloat("i", UNIT_SCALE=per_sec_unit_scale),
        BFloat("j", UNIT_SCALE=per_sec_unit_scale),
        BFloat("k", UNIT_SCALE=per_sec_unit_scale),
        SIDETIP="[0,+inf]", ORIENT="h"
        ),
    )

jpt__body = dict(jpt__body)
jpt__body[16] = damage
    
def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">", tag_cls=HekTag,
    )
