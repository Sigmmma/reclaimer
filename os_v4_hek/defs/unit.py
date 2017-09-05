from ...os_v3_hek.defs.unit import *

region_targeting_comment="""
When a target region is defined, melee damage is directed at it until it is destroyed.
"""

unit_keyframe_action = Struct("unit keyframe action",
    SEnum16("keyframe",
        "primary",
        "secondary",
        "final",
        ),
    Bool16("flags",
        "eject mounted units",
        ),
    SEnum16("target",
        "all seats",
        "mounted trigger seats",
        ),
    Pad(2),

    dependency('damage effect', "jpt!"),
    dependency('effect', "effe"),
    ascii_str32("effect marker"),
    SIZE=96
    )

seat_keyframe_action = Struct("seat keyframe action",
    SEnum16("keyframe",
        "primary",
        "secondary",
        "final",
        ),
    Bool16("flags",
        "control powered seat",
        ),
    SEnum16("self seat action",
        "none",
        "exit current seat",
        "enter target seat",
        ),
    SEnum16("target seat unit action",
        "none",
        "exit seat",
        "eject from seat",
        ),
    SEnum16("unit door action",
        "neither",
        "open",
        "close",
        ),
    Pad(2),
    SEnum16("apply damage to",
        "none",
        "mounted unit",
        "mounted unit region",
        "seated unit",
        ),
    Pad(2),

    ascii_str32("region name"),
    dependency('damage effect', "jpt!"),

    SEnum16("apply effect to",
        "none",
        "mounted unit",
        "seated unit",
        ),
    Pad(2),

    dependency('effect', "effe"),
    ascii_str32("effect marker"),

    SIZE=152
    )

mounted_state = Struct("mounted state",
    Bool16("flags",
        "third person camera"
        ),
    Pad(2),

    ascii_str32("camera marker name"),
    ascii_str32("camera submerged marker name"),
    float_deg("pitch autolevel"),
    from_to_deg("pitch range"),
    reflexive("camera tracks", camera_track, 2,
        'loose', 'tight'),
    reflexive("keyframe actions", unit_keyframe_action, 12,
        DYN_NAME_PATH='.effect_marker'),
    SIZE=128
    )

seat_access = Struct("seat access",
    Bool16("flags",
        "requires target seat occupied",
        "enemy access only",
        "restrict by unit sight",
        "restrict by mounting unit sight",
        "restrict by unit shield",
        "restrict by unit health",
        "restrict by ai state",
        ),
    Pad(2),
    float_rad("unit sight angle"),
    ascii_str32("unit sight marker name"),
    float_rad("mounting unit sight angle"),
    ascii_str32("mounting unit sight marker name"),
    float_zero_to_one("unit shield threshold"),
    float_zero_to_one("unit health threshold"),
    Bool16("permitted ai states", *actor_states),

    SIZE=124
    )

seat_boarding = Struct("seat boarding",
    SEnum16("boarding type",
        "immediate",
        "delayed"
        ),
    Bool16("delay until",
        "empty target seat",
        "unit shield threshold",
        "unit health threshold",
        "region destroyed",
        ),
    SEnum16("unit vitality source",
        "mounted unit",
        "seated unit"
        ),
    Pad(2),

    float_zero_to_one("unit shield threshold"),
    float_zero_to_one("unit health threshold"),
    Pad(4),

    ascii_str32("region name"),
    Pad(24),

    reflexive("seat keyframe actions", seat_keyframe_action, 12,
        DYN_NAME_PATH='.region_name'),

    SIZE=112
    )

seat_damage = Struct("seat damage",
    Bool16("flags",
        "use weapon damage melee effect",
        "exit after grenade plant",
        ),
    Struct("melee damage",
        SEnum16("melee",
            "normal",
            "mounted unit",
            "target seat unit"
            ),
        dependency("damage effect", "jpt!"),
        ),

    Struct("grenade damage",
        SEnum16("grenade",
            "normal",
            "disabled",
            "plant on mounted unit",
            "plant on target seat unit"
            ),
        Bool16("disabled types",
            "fragmentation grenade",
            "plasma grenade",
            "custom grenade 1",
            "custom grenade 2",
            ),
        float_zero_to_inf("detonation time", UNIT_SCALE=sec_unit_scale),
        ascii_str32("attach marker"),
        ),

    Struct("region targeting",
        Bool16("flags",
            "disable grenades until destroyed"
            ),
        Pad(2),

        ascii_str32("region name"),
        dependency("damage effect", "jpt!"),
        COMMENT=region_targeting_comment
        ),
    SIZE=136
    )

unit_extension = Struct("unit extension",
    reflexive("mounted states", mounted_state, 1),
    SIZE=60
    )

seat_extension = Struct("seat extension",
    Bool16("flags",
        "triggers mounted state",
        "exit on unit death",
        "exit on target seat empty",
        "prevent death when unit dies",
        "ignored by seated ai",
        "ignored by mounted ai",
        "cant enter seats when occupied",
        ),
    dyn_senum16("target seat",
        DYN_NAME_PATH="tagdata.unit_attrs.seats.STEPTREE[DYN_I].label"),
    Pad(12),  # reflexive("unknown", unknown),
    reflexive("seat access", seat_access, 1),
    reflexive("seat boarding", seat_boarding, 1),
    reflexive("seat damage", seat_damage, 1),
    SIZE=100
    )

seat = dict(seat)
unit_attrs = dict(unit_attrs)

seat[0] = Bool32("flags",
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
    "allow ai noncombatants",
    ("allows_melee", 1<<20)
    )
seat[20] = reflexive("seat extensions", seat_extension, 1)
unit_attrs[45] = reflexive("unit extensions", unit_extension, 1)
unit_attrs[54] = reflexive("seats", seat, 16, DYN_NAME_PATH='.label')

unit_body = Struct('tagdata', unit_attrs)

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
