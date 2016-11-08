from .obje import *
from .item import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=2)

magazine_item = Struct("magazine item",
    BSInt16("rounds"),

    Pad(10),
    dependency('equipment', "eqip"),
    SIZE=28
    )

magazine = Struct("magazine",
    BBool32("flags",
        "wastes rounds when reloaded",
        "every round must be chambered"
        ),
    BSInt16("rounds recharged"),
    BSInt16("rounds total initial"),
    BSInt16("rounds total maximum"),
    BSInt16("rounds loaded maximum"),

    Pad(8),
    BFloat("reload time"),
    BSInt16("rounds reloaded"),

    Pad(2),
    BFloat("chamber time"),

    Pad(24),
    dependency('reloading effect', valid_event_effects),
    dependency('chambering effect', valid_event_effects),

    Pad(12),
    reflexive("magazine item", magazine_item, 2,
        "primary", "secondary"),
    SIZE=112
    )

firing_effect = Struct("firing_effect",
    BSInt16("shot count lower bound"),
    BSInt16("shot count upper bound"),

    Pad(32),
    dependency('firing effect', valid_event_effects),
    dependency('misfire effect', valid_event_effects),
    dependency('empty effect', valid_event_effects),
    dependency('firing damage', "jpt!"),
    dependency('misfire damage', "jpt!"),
    dependency('empty damage', "jpt!"),
    SIZE=132
    )

trigger = Struct("trigger",
    BBool32("flags",
        "tracks fired projectile",
        "random firing effects",
        "can fire with partial ammo",
        "does not repeat automatically",
        "locks in on/off state",
        "projectiles use weapon origin",
        "sticks when dropped",
        "ejects during chamber",
        "discharging spews",
        "analog rate of fire",
        "use error when unzoomed",
        "projectile vector cannot be adjusted",
        "projectiles have identical error",
        "projectile is client side only",
        ),
    Struct("firing",
        QStruct("rounds per second", INCLUDE=from_to),
        BFloat("acceleration time"),
        BFloat("deceleration time"),
        BFloat("blurred rate of fire"),

        Pad(8),
        BSInt16("magazine",
            'primary',
            'secondary',
            ('NONE', -1)
            ),
        BSInt16("rounds per shot"),
        BSInt16("minimum rounds loaded"),
        BSInt16("rounds between tracers"),

        Pad(6),
        BSEnum16("firing noise", *sound_volumes),
        QStruct("error", INCLUDE=from_to),
        BFloat("error acceleration time"),
        BFloat("error deceleration time"),
        ),

    Pad(8),
    Struct("charging",
        BFloat("charging time"),
        BFloat("charge hold time"),
        BSInt16("overcharged action",
            'none',
            'explode',
            'discharge',
            ),

        Pad(2),
        BFloat("charged illumination", MIN=0.0, MAX=1.0),
        BFloat("spew time"),
        dependency('charging effect', valid_event_effects),
        ),

    Struct("projectile",
        BSInt16("distribution function",
            'point',
            'horizontal fan',
            ),
        BSInt16("projectiles per shot"),
        BFloat("distribution angle"),  # degrees

        Pad(4),
        BFloat("minimum error"),  # radians
        QStruct("error angle", INCLUDE=from_to),  # radians
        QStruct("first person offset", INCLUDE=xyz_float),

        Pad(4),
        dependency('projectile', valid_objects),
        ),

    BFloat("ejection port recovery time"),
    BFloat("illumination recovery time"),

    Pad(12),
    BFloat("heat generated per round", MIN=0.0, MAX=1.0),
    BFloat("age generated per round", MIN=0.0, MAX=1.0),

    Pad(4),
    BFloat("overload time"),

    Pad(64),
    reflexive("firing effects", firing_effect, 8),

    SIZE=276
    )

weap_attrs = Struct("weap attrs",
    BBool32("flags",
        "vertical heat display",
        "mutually exclusive triggers",
        "attacks automatically on bump",
        "must be readied",
        "doesnt count toward maximum",
        "aim assists only when zoomed",
        "prevents grenade throwing",
        "must be picked up",
        "holds triggers when dropped",
        "cannot fire at maximum age",
        "secondary trigger overrides grenades",
        "does not depower active camo in multiplayer",  # obsolete
        "enables integrated night vision",
        "ai uses weapon melee damage"
        ),
    ascii_str32('label'),
    BSEnum16('secondary trigger mode',
        "normal",
        "slaved to primary",
        "inhibits primary",
        "loads alternate ammunition",
        "loads multiple primary ammunition",
        ),
    BSInt16("max alternate shots loaded"),
    BSEnum16('A in', *weapon_export_to),
    BSEnum16('B in', *weapon_export_to),
    BSEnum16('C in', *weapon_export_to),
    BSEnum16('D in', *weapon_export_to),
    BFloat("ready time"),
    dependency('ready effect', valid_event_effects),

    Struct("heat",
        BFloat("recovery threshold", MIN=0.0, MAX=1.0),
        BFloat("overheated threshold", MIN=0.0, MAX=1.0),
        BFloat("detonation threshold", MIN=0.0, MAX=1.0),
        BFloat("detonation fraction", MIN=0.0, MAX=1.0),
        BFloat("loss per second", MIN=0.0, MAX=1.0),
        BFloat("illumination", MIN=0.0, MAX=1.0),

        Pad(16),
        dependency('overheated', valid_event_effects),
        dependency('detonation', valid_event_effects),
        ),

    dependency('player melee damage', "jpt!"),
    dependency('player melee response', "jpt!"),
    Pad(8),
    dependency('actor firing parameters', "actv"),

    Struct("aiming",
        BFloat("near reticle range"),
        BFloat("far reticle range"),
        BFloat("intersection reticle range"),

        Pad(2),
        BSInt16("zoom levels"),
        QStruct("zoom ranges", INCLUDE=from_to),
        BFloat("autoaim angle"),  # radians
        BFloat("autoaim range"),
        BFloat("magnetism angle"),  # radians
        BFloat("magnetism range"),
        BFloat("deviation angle"),  # radians
        ),

    Pad(4),
    Struct("movement and ai targeting",
        BSEnum16('movement penalized',
            "always",
            "when zoomed",
            "when zoomed or reloading",
            ),
        Pad(2),
        BFloat("forward movement penalty"),
        BFloat("sideways movement penalty"),

        Pad(4),
        BFloat("ai minimum target range"),
        BFloat("ai looking time modifier")
        ),

    Pad(4),
    Struct("misc",
        BFloat("light power-on time"),
        BFloat("light power-off time"),
        dependency('light power-on effect', valid_event_effects),
        dependency('light power-off effect', valid_event_effects),
        BFloat("age heat penalty"),
        BFloat("age rate of fire penalty"),
        BFloat("age misfire start", MIN=0.0, MAX=1.0),
        BFloat("age misfire chance", MIN=0.0, MAX=1.0)
        ),

    Pad(12),
    Struct("interface",
        dependency('first person model', valid_models),
        dependency('first person animations', "antr"),

        Pad(4),
        dependency('hud interface', "wphi"),
        dependency('pickup sound', "snd!"),
        dependency('zoom-in sound', "snd!"),
        dependency('zoom-out sound', "snd!"),

        Pad(12),
        BFloat('active camo ding'),
        BFloat('active camo regrowth rate'),
        ),

    Pad(14),
    BSEnum16('weapon type', *weapon_types),

    reflexive("predicted resources", predicted_resource),
    reflexive("magazines", magazine, 2,
        "primary", "secondary"),
    reflexive("triggers", trigger, 2,
        "primary", "secondary"),
    
    SIZE=512
    )

weap_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    weap_attrs,
    SIZE=1288,
    )


def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">"
    )
