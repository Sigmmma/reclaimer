from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

cdmg_body = Struct("tagdata",
    Struct("radius", INCLUDE=from_to),
    BFloat("cutoff scale"),  # [0.0 to 1.0]
    Pad(24),

    Struct("vibrate parameters",
        BFloat("low frequency"),
        BFloat("high frequency"),
        Pad(24),
        ),

    Struct("camera shaking",
        BFloat("random translation"),
        BFloat("random rotation"),  # measured in radians
        Pad(12),

        BSEnum16("wobble function", *animation_functions),
        Pad(2),
        BFloat("wobble function period"),
        BFloat("wobble weight"),
        Pad(192),
        ),

    Struct("damage",
        BSEnum16("priority",
            "none",
            "harmless",
            {NAME: "backstab", GUI_NAME: "lethal to the unsuspecting"},
            "emp",
            ),
        BSEnum16("category", *damage_category),
        BBool32("flags",
            "does not hurt owner",
            {NAME: "headshot", GUI_NAME: "can cause headshots"},
            "pings resistant units",
            "does not hurt friends",
            "does not ping shields",
            "detonates explosives",
            "only hurts shields",
            "causes flaming death",
            {NAME: "indicator_points_down",
             GUI_NAME: "damage indicators always point down"},
            "skips shields",
            "only hurts one infection form",
            {NAME: "multiplayer headshot",
             GUI_NAME: "can cause multiplayer headshots"},
            "infection form pop",
            ),
        Pad(4),
        BFloat("damage lower bound"),
        Struct("damage upper bound", INCLUDE=from_to),
        BFloat("vehicle passthrough penalty"),
        BFloat("active camouflage damage"),
        BFloat("stun"),
        BFloat("maximum stun"),
        BFloat("stun time"),
        Pad(4),
        BFloat("instantaneous acceleration"),
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

    ext=".continuous_damage_effect", endian=">",
    )
