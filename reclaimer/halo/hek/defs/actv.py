from ...common_descs import *
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
        BFloat("initial crouch chance", MIN=0.0, MAX=1.0),
        QStruct("crouch time", INCLUDE=from_to),
        QStruct("run time", INCLUDE=from_to)
        ),

    #Ranged combat
    Struct("ranged combat",
        dependency("weapon", "weap"),
        BFloat("maximum firing distance"),
        BFloat("rate of fire"),
        BFloat("projectile error"),  # radians
        QStruct("first burst delay time", INCLUDE=from_to),  # seconds
        BFloat("new-target firing pattern time"),
        BFloat("surprise delay time"),
        BFloat("surprise fire-wildly time"),
        BFloat("death fire-wildly chance", MIN=0.0, MAX=1.0),
        BFloat("death fire-wildly time"),  # seconds
        QStruct("desired combat range", INCLUDE=from_to),
        QStruct("custom stand gun offset", INCLUDE=ijk_float),
        QStruct("custom crouch gun offset", INCLUDE=ijk_float),
        BFloat("target tracking"),
        BFloat("target leading"),
        BFloat("weapon damage modifier"),
        BFloat("damage per second")
        ),

    #Burst geometry
    Struct("burst geometry",
        BFloat("burst origin radius"),
        BFloat("burst origin angle"),  # radians
        QStruct("burst return length", INCLUDE=from_to),
        BFloat("burst return angle"),  # radians
        QStruct("burst duration", INCLUDE=from_to),
        QStruct("burst separation", INCLUDE=from_to),
        BFloat("burst angular velocity"),  # radians/second
        Pad(4),
        BFloat("special damage modifier"),
        BFloat("special projectile error")  # radians
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
        BFloat("special-fire chance"),
        BFloat("special-fire delay")
        ),

    #Berserking and melee
    Struct("berserking and melee",
        BFloat("melee range"),
        BFloat("melee abort range"),
        QStruct("berserk firing ranges", INCLUDE=from_to),
        BFloat("berserk melee range"),
        BFloat("berserk melee abort range")
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
        BFloat("enemy radius"),

        Pad(4),
        BFloat("grenade velocity"),
        QStruct("grenade ranges", INCLUDE=from_to),
        BFloat("collateral damage radius"),
        BFloat("grenade chance", MIN=0.0, MAX=1.0),
        BFloat("grenade check time"),
        BFloat("encounter grenade timeout")
        ),

    #Items
    Struct("items",
        Pad(20),
        dependency("equipment", "eqip"),
        QStruct("grenade count",
            BSInt16("from", GUI_NAME=" "), BSInt16("to"), ORIENT='h'
            ),
        BFloat("dont drop grenades chance", MIN=0.0, MAX=1.0),
        QStruct("drop weapon loaded", INCLUDE=from_to),
        QStruct("drop weapon ammo",
            BSInt16("from", GUI_NAME=" "), BSInt16("to"), ORIENT='h'
            )
        ),

    #Unit properties
    Struct("unit properties",
        Pad(28),
        BFloat("body vitality"),
        BFloat("shield vitality"),
        BFloat("shield sapping radius"),
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

    ext=".actor_variant", endian=">"
    )
