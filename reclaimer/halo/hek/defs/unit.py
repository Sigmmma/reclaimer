from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return unit_def

camera_track = Struct('camera track',
    dependency('track', "trak"),
    SIZE=28
    )

new_hud_interface = Struct('new hud interface',
    dependency('unit hud interface', "unhi"),
    SIZE=48
    )

dialogue_variant = Struct('dialogue variant',
    BSInt16('variant number'),
    Pad(6),
    dependency('dialogue', "udlg"),
    SIZE=24
    )

powered_seat = Struct('powered seat',
    Pad(4),
    BFloat('driver powerup time'),
    BFloat('driver powerdown time'),
    SIZE=68
    )

weapon = Struct('weapon',
    dependency('weapon', "weap"),
    SIZE=36
    )

seat = Struct('seat',
    BBool32("flags",
        "invisible",
        "locked",
        "driver",
        "gunner",
        "third person camera",
        "allows weapons",
        "third person on enter",
        "first person slaved to gun",
        "allow vehicle communcation animation",
        "not valid without driver",
        "allow ai noncombatants"
        ),
    ascii_str32('label'),
    ascii_str32('marker name'),

    Pad(32),
    QStruct("acceleration scale", INCLUDE=ijk_float),

    Pad(12),
    BFloat('yaw rate'),  # degrees per second
    BFloat('pitch rate'),  # degrees per second
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    BFloat('pitch auto-level'),  # radians
    QStruct('pitch range', INCLUDE=from_to),  # radians

    reflexive("camera tracks", camera_track, 2,
              'loose', 'tight'),
    reflexive("new hud interfaces", new_hud_interface, 2,
              'default/solo', 'multiplayer'),

    Pad(4),
    BSInt16("hud text message index"),

    Pad(2),
    BFloat('yaw minimum'),
    BFloat('yaw maximum'),
    dependency('built-in gunner', "actv"),
    SIZE=284
    )

unit_attrs = Struct("unit attrs",
    BBool32("flags",
        "circular aiming",
        "destroyed after dying",
        "half-speed interpolation",
        "fires from camera",
        "entrance inside bounding sphere",
        "unused",
        "causes passenger dialogue",
        "resists pings",
        "melee attack is fatal",
        "dont reface during pings",
        "has no aiming",
        "simple creature",
        "impact melee attaches to unit",
        "cannot open doors automatically",
        "melee attackers cannot attach",
        "not instantly killed by melee",
        "shield sapping",
        "runs around flaming",
        "inconsequential",
        "special cinematic unit",
        "ignored by autoaiming",
        "shields fry infection forms",
        "integrated light controls weapon",
        "integrated light lasts forever",
        ),
    BSEnum16('default team', *unit_teams),
    BSEnum16('constant sound volume', *sound_volumes),
    BFloat('rider damage fraction'),
    dependency('integrated light toggle', "effe"),
    BSEnum16('A in', *unit_inputs),
    BSEnum16('B in', *unit_inputs),
    BSEnum16('C in', *unit_inputs),
    BSEnum16('D in', *unit_inputs),
    BFloat('camera field of view'),  # radians
    BFloat('camera stiffness'),
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    BFloat('pitch auto-level'),  # radians
    QStruct('pitch range', INCLUDE=from_to),  # radians
    reflexive("camera tracks", camera_track, 2,
              'loose', 'tight'),

    #Miscellaneous
    QStruct("seat acceleration scale", INCLUDE=ijk_float),
    Pad(12),
    BFloat('soft ping threshold', MIN=0.0, MAX=1.0),
    BFloat('soft ping interrupt time'),  # seconds
    BFloat('hard ping threshold', MIN=0.0, MAX=1.0),
    BFloat('hard ping interrupt time'),  # seconds
    BFloat('hard death threshold', MIN=0.0, MAX=1.0),
    BFloat('hard death interrupt time'),  # seconds
    BFloat('feign death time'),  # seconds
    BFloat('distance of evade aim'),
    BFloat('distance of dive aim'),

    Pad(4),
    BFloat('stunned movement threshold', MIN=0.0, MAX=1.0),
    BFloat('feign death chance', MIN=0.0, MAX=1.0),
    BFloat('feign repeat chance', MIN=0.0, MAX=1.0),
    dependency('spawned actor', "actv"),
    QStruct("spawned actor count",
        BSInt16("from", GUI_NAME=""), BSInt16("to"), ORIENT='h',
        ),
    BFloat('spawned velocity'),
    BFloat('aiming velocity maximum'),  # degrees/second
    BFloat('aiming acceleration maximum'),  # degrees/second^2
    BFloat('casual aiming modifier', MIN=0.0, MAX=1.0),
    BFloat('looking velocity maximum'),  # degrees/second
    BFloat('looking acceleration maximum'),  # degrees/second^2

    Pad(8),
    BFloat('ai vehicle radius'),
    BFloat('ai danger radius'),
    dependency('melee damage', "jpt!"),
    BSEnum16('motion sensor blip size',
        "medium",
        "small",
        "large",
        ),

    Pad(14),
    reflexive("new hud interfaces", new_hud_interface, 2,
              'default/solo', 'multiplayer'),
    reflexive("dialogue variants", dialogue_variant, 16),

    #Grenades
    BFloat('grenade velocity'),
    BSEnum16('grenade type', *grenade_types),
    BSInt16('grenade count'),

    Pad(4),
    reflexive("powered seats", powered_seat, 2,
              "driver", "gunner"),
    reflexive("weapons", weapon, 4),
    reflexive("seats", seat, 16),

    SIZE=372
    )

unit_body = Struct('tagdata',
    unit_attrs,
    SIZE=372
    )

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">"
    )
