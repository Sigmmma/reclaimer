from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

cdmg_body = Struct("tagdata",
    from_to_wu("radius"),
    float_zero_to_one("cutoff scale"),
    Pad(24),

    QStruct("vibrate parameters",
        float_zero_to_one("low frequency"),
        float_zero_to_one("high frequency"),
        Pad(24),
        ),

    Struct("camera shaking",
        float_wu("random translation"),
        float_rad("random rotation"),  # radians
        Pad(12),

        SEnum16("wobble function", *animation_functions),
        Pad(2),
        float_sec("wobble function period"),
        Float("wobble weight"),
        Pad(192),
        ),

    Struct("damage",
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
        float_zero_to_inf("instantaneous acceleration"),
        Pad(8),
        ),

    damage_modifiers,
    SIZE=512,
    )

    
def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
