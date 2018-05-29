from .obje import *
from .item import *
from .objs.tag import HekTag

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=2)

magazine_item = Struct("magazine item",
    SInt16("rounds"),

    Pad(10),
    dependency('equipment', "eqip"),
    SIZE=28
    )

magazine = Struct("magazine",
    Bool32("flags",
        "wastes rounds when reloaded",
        "every round must be chambered"
        ),
    SInt16("rounds recharged", SIDETIP="per second"),
    SInt16("rounds total initial"),
    SInt16("rounds total maximum"),
    SInt16("rounds loaded maximum"),

    Pad(8),
    float_sec("reload time"),
    SInt16("rounds reloaded"),

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
    SInt16("shot count lower bound"),
    SInt16("shot count upper bound"),

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
    Bool32("flags",
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
            Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
            Float("to",   UNIT_SCALE=per_sec_unit_scale),
            ORIENT='h'
            ),
        float_sec("acceleration time"),
        float_sec("deceleration time"),
        Float("blurred rate of fire", UNIT_SCALE=per_sec_unit_scale),

        Pad(8),
        SEnum16("magazine",
            'primary',
            'secondary',
            ('NONE', -1),
            DEFAULT=-1
            ),
        SInt16("rounds per shot"),
        SInt16("minimum rounds loaded"),
        SInt16("rounds between tracers"),

        Pad(6),
        SEnum16("firing noise", *sound_volumes),
        from_to_zero_to_one("error"),
        float_sec("error acceleration time"),
        float_sec("error deceleration time"),
        ),

    Pad(8),
    Struct("charging",
        float_sec("charging time"),
        float_sec("charge hold time"),
        SEnum16("overcharged action",
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
        SEnum16("distribution function",
            'point',
            'horizontal fan',
            ),
        SInt16("projectiles per shot"),
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
    Bool32("flags",
        "vertical heat display",
        "mutually exclusive triggers",
        "attacks automatically on bump",
        "must be readied",
        "doesnt count toward maximum",
        "aim assists only when zoomed",
        "prevents grenade throwing",
        "must be picked up",
        "holds triggers when dropped",
        "prevents melee attack",
        "detonates when dropped",
        "cannot fire at maximum age",
        "secondary trigger overrides grenades",
        "does not depower active camo in multiplayer",  # obsolete
        "enables integrated night vision",
        "ai uses weapon melee damage"
        ),
    ascii_str32('label'),
    SEnum16('secondary trigger mode',
        "normal",
        "slaved to primary",
        "inhibits primary",
        "loads alternate ammunition",
        "loads multiple primary ammunition",
        ),
    SInt16("max alternate shots loaded"),
    SEnum16('A in', *weapon_export_to),
    SEnum16('B in', *weapon_export_to),
    SEnum16('C in', *weapon_export_to),
    SEnum16('D in', *weapon_export_to),
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
        SInt16("zoom levels"),
        QStruct("zoom ranges", INCLUDE=from_to),
        float_rad("autoaim angle"),  # radians
        float_wu("autoaim range"),  # world units
        float_rad("magnetism angle"),  # radians
        float_wu("magnetism range"),  # world units
        float_rad("deviation angle"),  # radians
        ),

    Pad(4),
    Struct("movement",
        SEnum16('penalized',
            "always",
            "when zoomed",
            "when zoomed or reloading",
            ),
        Pad(2),
        Float("forward penalty"),
        Float("sideways penalty"),
        ),

    Pad(4),
    Struct("ai targeting",
        Float("minimum target range"),
        Float("looking time modifier")
        ),

    Pad(4),
    Struct("light",
        float_sec('power-on time',  UNIT_SCALE=sec_unit_scale),
        float_sec('power-off time', UNIT_SCALE=sec_unit_scale),
        dependency('power-on effect', valid_event_effects),
        dependency('power-off effect', valid_event_effects)
        ),

    Struct("age",
        Float("heat penalty"),
        Float("rate of fire penalty"),
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
        Float('active camo ding'),
        Float('active camo regrowth rate', UNIT_SCALE=per_sec_unit_scale),
        ),

    Pad(14),
    SEnum16('weapon type', *weapon_types),

    reflexive("predicted resources", predicted_resource, 1024, VISIBLE=False),
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
