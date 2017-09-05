from ...common_descs import *
from .objs.tag import HekTag
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
    SInt16('variant number'),
    Pad(6),
    dependency('dialogue', "udlg"),
    SIZE=24
    )

powered_seat = Struct('powered seat',
    Pad(4),
    float_sec('driver powerup time'),
    float_sec('driver powerdown time'),
    SIZE=68
    )

weapon = Struct('weapon',
    dependency('weapon', "weap"),
    SIZE=36
    )

seat = Struct('seat',
    Bool32("flags",
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
    float_deg_sec('yaw rate',   UNIT_SCALE=per_sec_unit_scale),  # degrees/sec
    float_deg_sec('pitch rate', UNIT_SCALE=per_sec_unit_scale),  # degrees/sec
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    float_rad('pitch auto-level'),  # radians
    from_to_rad('pitch range'),  # radians

    reflexive("camera tracks", camera_track, 2, 'loose', 'tight'),
    reflexive("new hud interfaces", new_hud_interface, 2,
              'default/solo', 'multiplayer'),

    Pad(4),
    SInt16("hud text message index"),

    Pad(2),
    float_rad('yaw minimum'),  # radians
    float_rad('yaw maximum'),  # radians
    dependency('built-in gunner', "actv"),
    Pad(12),  # open sauce seat extension padding
    SIZE=284
    )

unit_attrs = Struct("unit attrs",
    Bool32("flags",
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
    SEnum16('default team', *unit_teams),
    SEnum16('constant sound volume', *sound_volumes),
    float_zero_to_inf('rider damage fraction'),
    dependency('integrated light toggle', "effe"),
    SEnum16('A in', *unit_inputs),
    SEnum16('B in', *unit_inputs),
    SEnum16('C in', *unit_inputs),
    SEnum16('D in', *unit_inputs),
    float_rad('camera field of view'),  # radians
    Float('camera stiffness'),
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    float_rad('pitch auto-level'),  # radians
    from_to_rad('pitch range'),  # radians
    reflexive("camera tracks", camera_track, 2,
              'loose', 'tight'),

    #Miscellaneous
    QStruct("seat acceleration scale", INCLUDE=ijk_float),
    Pad(12),
    float_zero_to_one('soft ping threshold'),  # [0,1]
    float_sec('soft ping interrupt time', UNIT_SCALE=sec_unit_scale),  # seconds
    float_zero_to_one('hard ping threshold'),  # [0,1]
    float_sec('hard ping interrupt time', UNIT_SCALE=sec_unit_scale),  # seconds
    float_zero_to_one('hard death threshold'),  # [0,1]
    float_zero_to_one('feign death threshold'),  # [0,1]
    float_sec('feign death time', UNIT_SCALE=sec_unit_scale),  # seconds
    float_wu('distance of evade aim'),  # world units
    float_wu('distance of dive aim'),  # world units

    Pad(4),
    float_zero_to_one('stunned movement threshold'),  # [0,1]
    float_zero_to_one('feign death chance'),  # [0,1]
    float_zero_to_one('feign repeat chance'),  # [0,1]
    dependency('spawned actor', "actv"),
    QStruct("spawned actor count",
        SInt16("from", GUI_NAME=""), SInt16("to"), ORIENT='h',
        ),
    float_wu_sec('spawned velocity'),  
    float_rad_sec('aiming velocity maximum',
                  UNIT_SCALE=irad_per_sec_unit_scale),  # radians/sec
    float_rad_sec_sq('aiming acceleration maximum',
                     UNIT_SCALE=irad_per_sec_sq_unit_scale),  # radians/sec^2
    float_zero_to_one('casual aiming modifier'),
    float_rad_sec('looking velocity maximum',
                  UNIT_SCALE=irad_per_sec_unit_scale),  # radians/sec
    float_rad_sec_sq('looking acceleration maximum',
                     UNIT_SCALE=irad_per_sec_sq_unit_scale),  # radians/sec^2

    Pad(8),
    Float('ai vehicle radius'),
    Float('ai danger radius'),
    dependency('melee damage', "jpt!"),
    SEnum16('motion sensor blip size',
        "medium",
        "small",
        "large",
        ),
    Pad(2),

    Pad(12),  # open sauce unit extension padding
    reflexive("new hud interfaces", new_hud_interface, 2,
        'default/solo', 'multiplayer'),
    reflexive("dialogue variants", dialogue_variant, 16,
        DYN_NAME_PATH='.dialogue.filepath'),

    #Grenades
    float_wu_sec('grenade velocity'),
    SEnum16('grenade type', *grenade_types),
    SInt16('grenade count', MIN=0),

    Pad(4),
    reflexive("powered seats", powered_seat, 2,
              "driver", "gunner"),
    reflexive("weapons", weapon, 4, DYN_NAME_PATH='.weapon.filepath'),
    reflexive("seats", seat, 16, DYN_NAME_PATH='.label'),

    SIZE=372
    )

unit_body = Struct('tagdata',
    unit_attrs,
    SIZE=372
    )

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
