from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef


frequency_vibration = Struct("",
    float_zero_to_one("frequency"),
    float_sec("duration"),
    SEnum16("fade function", *fade_functions),
    )

jpt__body = Struct("tagdata",
    from_to_wu("radius"),
    float_zero_to_one("cutoff scale"),
    Bool32("flags",
        "dont_scale_by_distance",
        ),
    Pad(20),

    #Screen Flash
    Struct("screen flash",
        SEnum16("type",
            "none",
            "lighten",
            "darken",
            "max",
            "min",
            "invert",
            "tint",
            ),
        SEnum16("priority",
            "low",
            "medium",
            "high",
            ),
        Pad(12),

        float_sec("duration"),
        SEnum16("fade function", *fade_functions),
        Pad(10),

        float_zero_to_one("maximum intensity"),
        Pad(4),

        QStruct("tint lower bound", INCLUDE=argb_float),
        ),

    Struct("low frequency vibrate", INCLUDE=frequency_vibration),
    Pad(10),
    Struct("high frequency vibrate", INCLUDE=frequency_vibration),
    Pad(30),

    Struct("temporary camera impulse",
        float_sec("duration"),
        SEnum16("fade function", *fade_functions),
        Pad(2),

        float_rad("rotation"),  # radians
        float_wu("pushback"),
        from_to_wu("jitter"),
        Pad(8),
        ),

    float_rad("permanent camera impulse angle"),
    Pad(16),

    Struct("camera shaking",
        float_sec("duration"),
        SEnum16("fade function", *fade_functions),
        Pad(2),

        float_wu("random translation"),
        float_rad("random rotation"),  # radians
        Pad(12),

        SEnum16("wobble function", *animation_functions),
        Pad(2),
        float_sec("wobble function period"),
        Float("wobble weight"),
        Pad(32),
        ),

    dependency("sound", "snd!"),
    Pad(112),

    QStruct("breaking effect",
        float_wu_sec("forward velocity"),
        float_wu("forward radius"),
        Float("forward exponent"),
        Pad(12),

        float_wu_sec("outward velocity"),
        float_wu("outward radius"),
        Float("outward exponent"),
        Pad(12),
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
            ),
        float_wu("aoe core radius"),
        Float("damage lower bound"),
        QStruct("damage upper bound", INCLUDE=from_to),
        float_zero_to_one("vehicle passthrough penalty"),
        float_zero_to_one("active camouflage damage"),
        float_zero_to_one("stun"),
        float_zero_to_one("maximum stun"),
        float_sec("stun time"),
        Pad(4),
        float_zero_to_inf("instantaneous acceleration"),
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

    ext=".damage_effect", endian=">", tag_cls=HekTag,
    )
