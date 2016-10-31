from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef


frequency_vibration = Struct("",
    BFloat("frequency", MIN=0.0, MAX=1.0),
    BFloat("duration"),
    BSEnum16("fade function", *fade_functions),
    )

jpt__body = Struct("tagdata",
    QStruct("radius", INCLUDE=from_to),
    BFloat("cutoff scale", MIN=0.0, MAX=1.0),
    BBool32("flags",
        "dont_scale_by_distance",
        ),
    Pad(20),

    #Screen Flash
    Struct("screen flash",
        BSEnum16("type",
            "none",
            "lighten",
            "darken",
            "max",
            "min",
            "invert",
            "tint",
            ),
        BSEnum16("priority",
            "low",
            "medium",
            "high",
            ),
        Pad(12),

        BFloat("duration"),
        BSEnum16("fade function", *fade_functions),
        Pad(10),

        BFloat("maximum intensity", MIN=0.0, MAX=1.0),
        Pad(4),

        QStruct("tint lower bound", INCLUDE=argb_float),
        ),

    Struct("low frequency vibrate", INCLUDE=frequency_vibration),
    Pad(10),
    Struct("high frequency vibrate", INCLUDE=frequency_vibration),
    Pad(30),

    Struct("temporary camera impulse",
        BFloat("duration"),
        BSEnum16("fade function", *fade_functions),
        Pad(2),

        BFloat("rotation"),  # measured in radians
        BFloat("pushback"),
        QStruct("jitter", INCLUDE=from_to),
        Pad(8),
        ),

    BFloat("permanent camera impulse angle"),
    Pad(16),

    Struct("camera shaking",
        BFloat("duration"),
        BSEnum16("fade function", *fade_functions),
        Pad(2),

        BFloat("random translation"),
        BFloat("random rotation"),  # measured in radians
        Pad(12),

        BSEnum16("wobble function", *animation_functions),
        Pad(2),
        BFloat("wobble function period"),
        BFloat("wobble weight"),
        Pad(32),
        ),

    dependency("sound", valid_sounds),
    Pad(112),

    QStruct("breaking effect",
        BFloat("forward velocity"),
        BFloat("forward radius"),
        BFloat("forward exponent"),
        Pad(12),

        BFloat("outward velocity"),
        BFloat("outward radius"),
        BFloat("outward exponent"),
        Pad(12),
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
            {NAME: "headshot", GUI_NAME: "causes headshots"},
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
             GUI_NAME: "causes multiplayer headshots"},
            "infection form pop",
            ),
        BFloat("aoe core radius"),
        BFloat("damage lower bound"),
        QStruct("damage upper bound", INCLUDE=from_to),
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
    SIZE=672,
    )

    
def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">",
    )
