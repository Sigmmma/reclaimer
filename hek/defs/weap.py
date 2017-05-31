from .obje import *
from .item import *
from .objs.tag import HekTag

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
    BSInt16("rounds recharged", SIDETIP="per second"),
    BSInt16("rounds total initial"),
    BSInt16("rounds total maximum"),
    BSInt16("rounds loaded maximum"),

    Pad(8),
    float_sec("reload time"),
    BSInt16("rounds reloaded"),

    Pad(2),
    float_sec("chamber time"),

    Pad(24),
    dependency('reloading effect', valid_event_effects),
    dependency('chambering effect', valid_event_effects),

    Pad(12),
    reflexive("magazine items", magazine_item, 2,
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
        QStruct("rounds per second",
            BFloat("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
            BFloat("to",   UNIT_SCALE=per_sec_unit_scale),
            ORIENT='h'
            ),
        float_sec("acceleration time"),
        float_sec("deceleration time"),
        BFloat("blurred rate of fire", UNIT_SCALE=per_sec_unit_scale),

        Pad(8),
        BSEnum16("magazine",
            'primary',
            'secondary',
            ('NONE', -1),
            DEFAULT=-1
            ),
        BSInt16("rounds per shot"),
        BSInt16("minimum rounds loaded"),
        BSInt16("rounds between tracers"),

        Pad(6),
        BSEnum16("firing noise", *sound_volumes),
        from_to_zero_to_one("error"),
        float_sec("error acceleration time"),
        float_sec("error deceleration time"),
        ),

    Pad(8),
    Struct("charging",
        float_sec("charging time"),
        float_sec("charge hold time"),
        BSEnum16("overcharged action",
            'none',
            'explode',
            'discharge',
            ),

        Pad(2),
        float_zero_to_one("charged illumination"),
        float_sec("spew time"),
        dependency('charging effect', valid_event_effects),
        ),

    Struct("projectile",
        BSEnum16("distribution function",
            'point',
            'horizontal fan',
            ),
        BSInt16("projectiles per shot"),
        float_deg("distribution angle"),  # degrees

        Pad(4),
        float_rad("minimum error"),  # radians
        from_to_rad("error angle"),  # radians
        QStruct("first person offset", INCLUDE=xyz_float),

        Pad(4),
        dependency('projectile', valid_objects),
        ),

    Struct("misc",
        float_sec("ejection port recovery time"),
        float_sec("illumination recovery time"),

        Pad(12),
        float_zero_to_one("heat generated per round"),
        float_zero_to_one("age generated per round"),

        Pad(4),
        float_sec("overload time"),

        Pad(64),
        reflexive("firing effects", firing_effect, 8),
        ),

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
    float_sec("ready time"),
    dependency('ready effect', valid_event_effects),

    Struct("heat",
        float_zero_to_one("recovery threshold"),
        float_zero_to_one("overheated threshold"),
        float_zero_to_one("detonation threshold"),
        float_zero_to_one("detonation fraction"),
        float_zero_to_one("loss per second", UNIT_SCALE=per_sec_unit_scale),
        float_zero_to_one("illumination"),

        Pad(16),
        dependency('overheated', valid_event_effects),
        dependency('detonation', valid_event_effects),
        ),

    Struct("melee",
        dependency('player damage', "jpt!"),
        dependency('player response', "jpt!"),
        ),

    Pad(8),
    Struct("aiming",
        dependency("actor firing parameters", "actv"),
        float_wu("near reticle range"),  # world units
        float_wu("far reticle range"),  # world units
        float_wu("intersection reticle range"),  # world units

        Pad(2),
        BSInt16("zoom levels"),
        QStruct("zoom ranges", INCLUDE=from_to),
        float_rad("autoaim angle"),  # radians
        float_wu("autoaim range"),  # world units
        float_rad("magnetism angle"),  # radians
        float_wu("magnetism range"),  # world units
        float_rad("deviation angle"),  # radians
        ),

    Pad(4),
    Struct("movement",
        BSEnum16('penalized',
            "always",
            "when zoomed",
            "when zoomed or reloading",
            ),
        Pad(2),
        BFloat("forward penalty"),
        BFloat("sideways penalty"),
        ),

    Pad(4),
    Struct("ai targeting",
        BFloat("minimum target range"),
        BFloat("looking time modifier")
        ),

    Pad(4),
    Struct("light",
        float_sec('power-on time',  UNIT_SCALE=sec_unit_scale),
        float_sec('power-off time', UNIT_SCALE=sec_unit_scale),
        dependency('power-on effect', valid_event_effects),
        dependency('power-off effect', valid_event_effects)
        ),

    Struct("age",
        BFloat("heat penalty"),
        BFloat("rate of fire penalty"),
        float_zero_to_one("misfire start"),
        float_zero_to_one("misfire chance")
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
        BFloat('active camo regrowth rate', UNIT_SCALE=per_sec_unit_scale),
        ),

    Pad(14),
    BSEnum16('weapon type', *weapon_types),

    reflexive("predicted resources", predicted_resource, 1024),
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

    ext=".weapon", endian=">", tag_cls=HekTag
    )
