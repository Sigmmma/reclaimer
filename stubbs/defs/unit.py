'''
THIS DEFINITION IS INCORRECT BECAUSE THE UNIT STRUCTURE IS DIFFERENT THAN HALO'S
'''

from ...hek.defs.unit import *
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

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
        "unknown24",
        "unknown25"
        ),
    ascii_str32('unknown1'),
    BSEnum16('default team', *unit_teams),
    BSEnum16('constant sound volume', *sound_volumes),
    float_zero_to_inf('rider damage fraction'),
    dependency('integrated light toggle', "effe"),
    BSEnum16('A in', *unit_inputs),
    BSEnum16('B in', *unit_inputs),
    BSEnum16('C in', *unit_inputs),
    BSEnum16('D in', *unit_inputs),
    float_rad('camera field of view'),  # radians
    BFloat('camera stiffness'),
    ascii_str32('camera marker name'),
    ascii_str32('camera submerged marker name'),
    float_rad('pitch auto-level'),  # radians
    from_to_rad('pitch range'),  # radians
    reflexive("camera tracks", camera_track, 2,
              'loose', 'tight'),

    BytearrayRaw('unknown2', SIZE=68),

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
        BSInt16("from", GUI_NAME=""), BSInt16("to"), ORIENT='h',
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
    BFloat('ai vehicle radius'),
    BFloat('ai danger radius'),
    dependency('melee damage', "jpt!"),
    BSEnum16('motion sensor blip size',
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
    BSEnum16('grenade type', *grenade_types),
    BSInt16('grenade count', MIN=0),

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

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">"
    )
