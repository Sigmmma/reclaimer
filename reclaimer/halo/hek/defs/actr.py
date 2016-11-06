from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

danger_triggers = (
    "never",
    "visible",
    "shooting",
    "shooting near us",
    "damaging us",
    "unused1",
    "unused2",
    "unused3",
    "unused4",
    "unused5",
    )

actr_body = Struct("tagdata",
    BBool32('flags',
        "can see in darkness",
        "sneak uncovering target",
        "sneak uncovering pursuit location",
        "unused1",
        "shoot at targets last location",
        "try to stay still when crouched",
        "crouch when not in combat",
        "crouch when guarding",
        "unused2",
        "must crouch to shoot",
        "panic when surprised",
        "always charge at enemies",
        "gets in vehicles with player",
        "starts firing before aligned",
        "standing must move forward",
        "crouching must move forward",
        "defensive crouch while charging",
        "use stalking behavior",
        "stalking freeze if exposed",
        "always berserk in attacking mode",
        "berserking uses panicked movement",
        "flying",
        "panicked by unopposable enemy",
        "crouch when hiding from unopposable",
        "always charge in attacking mode",
        "dive off ledges",
        "swarm",
        "suicidal melee attack",
        "cannot move while crouching",
        "fixed crouch facing",
        "crouch when in line of fire",
        "avoid friends line of fire"
        ),
    BBool32('more flags',
        "avoid all enemy attack vectors",
        "must stand to fire",
        "must stop to fire",
        "disallow vehicle combat",
        "pathfinding ignores danger",
        "panic in groups",
        "no corpse shooting"
        ),

    Pad(12),
    BSEnum16("type", *actor_types),

    Pad(2),
    Struct("perception",
        BFloat("max vision distance"),  # world units
        BFloat("central vision angle"),  # radians
        BFloat("max vision angle"),  # radians

        Pad(4),
        BFloat("peripheral vision angle"),  # radians
        BFloat("peripheral distance"),  # world units

        Pad(4),
        QStruct("standing gun offset", INCLUDE=ijk_float),
        QStruct("crouching gun offset", INCLUDE=ijk_float),
        BFloat("hearing distance"),  # world units
        BFloat("notice projectile chance", MIN=0.0, MAX=1.0),
        BFloat("notice vehicle chance", MIN=0.0, MAX=1.0),

        Pad(8),
        BFloat("combat perception time"),  # seconds
        BFloat("guard perception time"),  # seconds
        BFloat("non-combat perception time"),  # seconds
        ),

    Pad(20),
    Struct("movement",
        BFloat("dive into cover chance", MIN=0.0, MAX=1.0),
        BFloat("emerge from cover chance", MIN=0.0, MAX=1.0),
        BFloat("dive from grenade cover chance", MIN=0.0, MAX=1.0),
        BFloat("pathfinding radius"),  # world units
        BFloat("glass ignorance chance", MIN=0.0, MAX=1.0),
        BFloat("stationary movement dist"),  # world units
        BFloat("free-flying sidestep"),  # world units
        BFloat("begin moving angle"),  # radians
        ),

    Pad(4),
    Struct("looking",
        QStruct("maximum aiming deviation", INCLUDE=yp_float),  # radians
        QStruct("maximum looking deviation", INCLUDE=yp_float),  # radians
        BFloat("noncombat look delta l"),  # radians
        BFloat("noncombat look delta r"),  # radians
        BFloat("combat look delta l"),  # radians
        BFloat("combat look delta r"),  # radians
        QStruct("idle aiming range", INCLUDE=from_to),  # radians
        QStruct("idle looking range", INCLUDE=from_to),  # radians
        QStruct("event look time modifier", INCLUDE=from_to),
        QStruct("noncombat idle facing", INCLUDE=from_to),  # seconds
        QStruct("noncombat idle aiming", INCLUDE=from_to),  # seconds
        QStruct("noncombat idle looking", INCLUDE=from_to),  # seconds
        QStruct("guard idle facing", INCLUDE=from_to),  # seconds
        QStruct("guard idle aiming", INCLUDE=from_to),  # seconds
        QStruct("guard idle looking", INCLUDE=from_to),  # seconds
        QStruct("combat idle facing", INCLUDE=from_to),  # seconds
        QStruct("combat idle aiming", INCLUDE=from_to),  # seconds
        QStruct("combat idle looking", INCLUDE=from_to),  # seconds

        Pad(24),
        dependency("DO NOT USE 1", "weap"),

        Pad(268),
        dependency("DO NOT USE 2", "proj")
        ),

    Struct("unopposable",
        BSEnum16("unreachable danger trigger", *danger_triggers),
        BSEnum16("vehicle danger trigger", *danger_triggers),
        BSEnum16("player danger trigger", *danger_triggers),

        Pad(2),
        QStruct("danger trigger time", INCLUDE=from_to),  # seconds
        BSInt16("friends killed trigger"),
        BSInt16("friends retreating trigger"),

        Pad(12),
        QStruct("retreat time", INCLUDE=from_to),  # seconds
        ),

    Pad(8),
    Struct("panic",
        QStruct("cowering time", INCLUDE=from_to),  # seconds
        BFloat("friend killed panic chance", MIN=0.0, MAX=1.0),
        BSEnum16("leader type", *actor_types),

        Pad(2),
        BFloat("leader killed panic chance", MIN=0.0, MAX=1.0),
        BFloat("panic damage threshold", MIN=0.0, MAX=1.0),
        BFloat("surprise distance"),  # world units
        ),

    Pad(28),
    Struct("defensive",
        QStruct("hide behind cover time", INCLUDE=from_to),  # seconds
        BFloat("hide target-not-visible time"),  # seconds
        BFloat("hide shield fraction", MIN=0.0, MAX=1.0),
        BFloat("attack shield fraction", MIN=0.0, MAX=1.0),
        BFloat("pursue shield fraction", MIN=0.0, MAX=1.0),

        Pad(16),
        BSEnum16("defensive crouch type",
            "never",
            "danger",
            "low shields",
            "hide behind shield",
            "any target",
            "flood shamble"
            ),

        Pad(2),
        BFloat("attacking crouch threshold"),
        BFloat("defending crouch threshold"),
        BFloat("mim stand time"),  # seconds
        BFloat("mim crouch time"),  # seconds
        BFloat("defending hide time modifier"),
        BFloat("attacking evasion threshold"),
        BFloat("defending evasion threshold"),
        BFloat("evasion seek-cover chance", MIN=0.0, MAX=1.0),
        BFloat("evasion delay time"),  # seconds
        BFloat("max seek cover distance"),  # world units
        BFloat("cover damage threshold", MIN=0.0, MAX=1.0),
        BFloat("stalking discovery time"),  # seconds
        BFloat("stalking max distance"),  # world units
        BFloat("stationary facing angle"),  # radians
        BFloat("change facing stand time"),  # seconds
        ),

    Pad(4),
    Struct("pursuit",
        QStruct("uncover delay time", INCLUDE=from_to),  # seconds
        QStruct("target search time", INCLUDE=from_to),  # seconds
        QStruct("pursuit position time", INCLUDE=from_to),  # seconds
        BSInt16("coordinated position count", MIN=0),
        BSInt16("normal position count", MIN=0),
        ),

    Pad(32),
    QStruct("berserk",
        BFloat("melee attack delay"),  # seconds
        BFloat("melee fudge factor"),  # world units
        BFloat("melee charge time"),  # seconds
        BFloat("melee leap range lower bound"),  # world units
        BFloat("melee leap range upper bound"),  # world units
        BFloat("melee leap velocity"),  # world units/tick
        BFloat("melee leap chance", MIN=0.0, MAX=1.0),
        BFloat("melee leap ballistic", MIN=0.0, MAX=1.0),
        BFloat("berserk damage amount", MIN=0.0, MAX=1.0),
        BFloat("berserk damage threshold", MIN=0.0, MAX=1.0),
        BFloat("berserk proximity"),  # world units
        BFloat("suicide sensing dist"),  # world units
        BFloat("berserk grenade chance", MIN=0.0, MAX=1.0),
        ),

    Pad(12),
    Struct("firing positions",
        QStruct("guard position time", INCLUDE=from_to),  # seconds
        QStruct("combat position time", INCLUDE=from_to),  # seconds
        BFloat("old position avoid dist"),  # world units
        BFloat("friend avoid dist"),  # world units
        ),

    Pad(40),
    Struct("communication",
        QStruct("noncombat idle speech time", INCLUDE=from_to),  # seconds
        QStruct("combat idle speech time", INCLUDE=from_to),  # seconds

        Pad(176),
        dependency("DO NOT USE 3", "actr"),
        ),
    SIZE=1272
    )


def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header('actr'),
    actr_body,

    ext=".actor", endian=">"
    )
