from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

change_color = Struct("change_color",
    QStruct("color lower bound", INCLUDE=rgb_float),
    QStruct("color upper bound", INCLUDE=rgb_float),
    SIZE=32
    )

actv_body = Struct("tagdata",
    BBool32('flags',
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
        BSEnum16("movement type",
            "always run",
            "always crouch",
            "switch types",
            ),
        Pad(2),
        float_zero_to_one("initial crouch chance"),
        from_to_sec("crouch time"),
        from_to_sec("run time")
        ),

    #Ranged combat
    Struct("ranged combat",
        dependency("weapon", "weap"),
        float_wu("maximum firing distance"),
        BFloat("rate of fire"),
        float_rad("projectile error"),  # radians
        from_to_sec("first burst delay time"),  # seconds
        BFloat("new-target firing pattern time"),
        BFloat("surprise delay time"),
        BFloat("surprise fire-wildly time"),
        float_zero_to_one("death fire-wildly chance"),
        float_sec("death fire-wildly time"),  # seconds
        from_to_wu("desired combat range"),
        QStruct("custom stand gun offset", INCLUDE=ijk_float),
        QStruct("custom crouch gun offset", INCLUDE=ijk_float),
        float_zero_to_one("target tracking"),
        float_zero_to_one("target leading"),
        BFloat("weapon damage modifier"),
        BFloat("damage per second")
        ),

    #Burst geometry
    Struct("burst geometry",
        float_wu("burst origin radius"),
        float_rad("burst origin angle"),  # radians
        from_to_sec("burst return length"),
        float_rad("burst return angle"),  # radians
        from_to_sec("burst duration"),
        from_to_sec("burst separation"),
        BFloat("burst angular velocity",
            SIDETIP="degrees/sec", UNIT_SCALE=180/pi),  # radians/second
        Pad(4),
        float_zero_to_one("special damage modifier"),
        float_rad("special projectile error")  # radians
        ),

    #Firing patterns"
    Struct("firing patterns",
        BFloat("new-target burst duration"),
        BFloat("new-target burst separation"),
        BFloat("new-target rate of fire"),
        BFloat("new-target projectile error"),

        Pad(8),
        BFloat("moving burst duration"),
        BFloat("moving burst separation"),
        BFloat("moving rate of fire"),
        BFloat("moving projectile error"),

        Pad(8),
        BFloat("berserk burst duration"),
        BFloat("berserk burst separation"),
        BFloat("berserk rate of fire"),
        BFloat("berserk projectile error")
        ),

    #Special-case firing patterns
    Struct("special case firing patterns",
        Pad(8),
        BFloat("super-ballistic range"),
        BFloat("bombardment range"),
        BFloat("modified vision range"),
        BSEnum16("special-fire mode",
            "none",
            "overcharge",
            "secondary trigger",
            ),
        BSEnum16("special-fire situation",
            "never",
            "enemy visible",
            "enemy out of sight",
            "strafing",
            ),
        float_zero_to_one("special-fire chance"),
        float_sec("special-fire delay")
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
        BSEnum16("grenade type", *grenade_types),
        BSEnum16("trajectory type",
            "toss",
            "lob",
            "bounce",
            ),
        BSEnum16("grenade stimulus",
            "never",
            "visible target",
            "seek cover",
            ),
        BSInt16("minimum enemy count"),
        float_wu("enemy radius"),

        Pad(4),
        float_wu_sec("grenade velocity"),
        from_to_wu("grenade ranges"),
        float_wu("collateral damage radius"),
        float_zero_to_one("grenade chance"),
        float_sec("grenade check time"),
        float_sec("encounter grenade timeout")
        ),

    #Items
    Struct("items",
        Pad(20),
        dependency("equipment", "eqip"),
        QStruct("grenade count",
            BSInt16("from", GUI_NAME=""), BSInt16("to"), ORIENT='h'
            ),
        float_zero_to_one("dont drop grenades chance"),
        QStruct("drop weapon loaded", INCLUDE=from_to),
        QStruct("drop weapon ammo",
            BSInt16("from", GUI_NAME=""),
            BSInt16("to"), ORIENT='h'
            )
        ),

    #Unit properties
    Struct("unit properties",
        Pad(28),
        BFloat("body vitality"),
        BFloat("shield vitality"),
        float_wu("shield sapping radius"),
        BSInt16("forced shader permutation"),
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
