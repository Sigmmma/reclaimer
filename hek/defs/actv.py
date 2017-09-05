from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

change_color = Struct("change_color",
    QStruct("color lower bound", INCLUDE=rgb_float),
    QStruct("color upper bound", INCLUDE=rgb_float),
    SIZE=32
    )

actv_body = Struct("tagdata",
    Bool32('flags',
        "can shoot while flying",
        "blend color in hsv",
        "has unlimited grenades",
        "moveswitch stay with friends",
        "active camouflage",
        "super active camouflage",
        "cannot use ranged weapons",
        "prefer passenger seat",
        ),
    dependency("actor definition", "actr"),
    dependency("unit", valid_units),
    dependency("major variant", "actv"),

    #Movement switching
    Struct("movement switching",
        Pad(24),
        SEnum16("movement type",
            "always run",
            "always crouch",
            "switch types",
            ),
        Pad(2),
        float_zero_to_one("initial crouch chance"),
        from_to_sec("crouch time", UNIT_SCALE=sec_unit_scale),  # seconds
        from_to_sec("run time",    UNIT_SCALE=sec_unit_scale)   # seconds
        ),

    #Ranged combat
    Struct("ranged combat",
        dependency("weapon", "weap"),
        float_wu("maximum firing distance"),
        Float("rate of fire", UNIT_SCALE=per_sec_unit_scale),  # rounds/sec
        float_rad("projectile error"),  # radians
        from_to_sec("first burst delay time",
                    UNIT_SCALE=sec_unit_scale),  # seconds
        Float("new-target firing pattern time",
               UNIT_SCALE=sec_unit_scale),  # seconds
        Float("surprise delay time", UNIT_SCALE=sec_unit_scale),  # seconds
        Float("surprise fire-wildly time",
               UNIT_SCALE=sec_unit_scale),  # seconds
        float_zero_to_one("death fire-wildly chance"),
        float_sec("death fire-wildly time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        from_to_wu("desired combat range"),
        QStruct("custom stand gun offset", INCLUDE=ijk_float),
        QStruct("custom crouch gun offset", INCLUDE=ijk_float),
        float_zero_to_one("target tracking"),
        float_zero_to_one("target leading"),
        Float("weapon damage modifier"),
        Float("damage per second", UNIT_SCALE=per_sec_unit_scale),  # seconds
        ),

    #Burst geometry
    Struct("burst geometry",
        float_wu("burst origin radius"),
        float_rad("burst origin angle"),  # radians
        from_to_sec("burst return length"),
        float_rad("burst return angle"),  # radians
        from_to_sec("burst duration", UNIT_SCALE=sec_unit_scale),  # seconds
        from_to_sec("burst separation"),
        Float("burst angular velocity", SIDETIP="degrees/sec",
               UNIT_SCALE=irad_per_sec_unit_scale), # radians/second
        Pad(4),
        float_zero_to_one("special damage modifier"),
        float_rad("special projectile error")  # radians
        ),

    #Firing patterns"
    Struct("firing patterns",
        Float("new-target burst duration"),
        Float("new-target burst separation"),
        Float("new-target rate of fire", UNIT_SCALE=per_sec_unit_scale),
        Float("new-target projectile error"),

        Pad(8),
        Float("moving burst duration"),
        Float("moving burst separation"),
        Float("moving rate of fire", UNIT_SCALE=per_sec_unit_scale),
        Float("moving projectile error"),

        Pad(8),
        Float("berserk burst duration"),
        Float("berserk burst separation"),
        Float("berserk rate of fire", UNIT_SCALE=per_sec_unit_scale),
        Float("berserk projectile error")
        ),

    #Special-case firing patterns
    Struct("special case firing patterns",
        Pad(8),
        Float("super-ballistic range"),
        Float("bombardment range"),
        Float("modified vision range"),
        SEnum16("special-fire mode",
            "none",
            "overcharge",
            "secondary trigger",
            ),
        SEnum16("special-fire situation",
            "never",
            "enemy visible",
            "enemy out of sight",
            "strafing",
            ),
        float_zero_to_one("special-fire chance"),
        float_sec("special-fire delay", UNIT_SCALE=sec_unit_scale)
        ),

    #Berserking and melee
    Struct("berserking and melee",
        float_wu("melee range"),
        float_wu("melee abort range"),
        from_to_wu("berserk firing ranges", INCLUDE=from_to),
        float_wu("berserk melee range"),
        float_wu("berserk melee abort range")
        ),

    #Grenades
    Struct("grenades",
        Pad(8),
        SEnum16("grenade type", *grenade_types),
        SEnum16("trajectory type",
            "toss",
            "lob",
            "bounce",
            ),
        SEnum16("grenade stimulus",
            "never",
            "visible target",
            "seek cover",
            ),
        SInt16("minimum enemy count"),
        float_wu("enemy radius"),

        Pad(4),
        float_wu_sec("grenade velocity", UNIT_SCALE=per_sec_unit_scale),
        from_to_wu("grenade ranges"),
        float_wu("collateral damage radius"),
        float_zero_to_one("grenade chance"),
        float_sec("grenade check time", UNIT_SCALE=sec_unit_scale),
        float_sec("encounter grenade timeout", UNIT_SCALE=sec_unit_scale)
        ),

    #Items
    Struct("items",
        Pad(20),
        dependency("equipment", "eqip"),
        QStruct("grenade count",
            SInt16("from", GUI_NAME=""), SInt16("to"), ORIENT='h'
            ),
        float_zero_to_one("dont drop grenades chance"),
        QStruct("drop weapon loaded", INCLUDE=from_to),
        QStruct("drop weapon ammo",
            SInt16("from", GUI_NAME=""),
            SInt16("to"), ORIENT='h'
            )
        ),

    #Unit properties
    Struct("unit properties",
        Pad(28),
        Float("body vitality"),
        Float("shield vitality"),
        float_wu("shield sapping radius"),
        SInt16("forced shader permutation"),
        ),

    Pad(30),
    reflexive("change_colors", change_color, 4),
    SIZE=568
    )


def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
