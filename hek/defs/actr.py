from ...common_descs import *
from .objs.tag import HekTag
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
    Bool32('flags',
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
    Bool32('more flags',
        "avoid all enemy attack vectors",
        "must stand to fire",
        "must stop to fire",
        "disallow vehicle combat",
        "pathfinding ignores danger",
        "panic in groups",
        "no corpse shooting"
        ),

    Pad(12),
    SEnum16("type", *actor_types),

    Pad(2),
    Struct("perception",
        float_wu("max vision distance"),  # world units
        float_rad("central vision angle"),  # radians
        float_rad("max vision angle"),  # radians

        Pad(4),
        float_rad("peripheral vision angle"),  # radians
        float_wu("peripheral distance"),  # world units

        Pad(4),
        QStruct("standing gun offset", INCLUDE=ijk_float),
        QStruct("crouching gun offset", INCLUDE=ijk_float),
        float_wu("hearing distance"),  # world units
        float_zero_to_one("notice projectile chance"),
        float_zero_to_one("notice vehicle chance"),

        Pad(8),
        float_sec("combat perception time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("guard perception time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("non-combat perception time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        ),

    Pad(20),
    Struct("movement",
        float_zero_to_one("dive into cover chance"),
        float_zero_to_one("emerge from cover chance"),
        float_zero_to_one("dive from grenade cover chance"),
        float_wu("pathfinding radius"),  # world units
        float_zero_to_one("glass ignorance chance"),
        float_wu("stationary movement dist"),  # world units
        float_wu("free-flying sidestep"),  # world units
        float_rad("begin moving angle"),  # radians
        ),

    Pad(4),
    Struct("looking",
        yp_float_rad("maximum aiming deviation"),  # radians
        yp_float_rad("maximum looking deviation"),  # radians
        float_rad("noncombat look delta l"),  # radians
        float_rad("noncombat look delta r"),  # radians
        float_rad("combat look delta l"),  # radians
        float_rad("combat look delta r"),  # radians
        from_to_rad("idle aiming range"),  # radians
        from_to_rad("idle looking range"),  # radians
        QStruct("event look time modifier", INCLUDE=from_to),
        from_to_sec("noncombat idle facing"),  # seconds
        from_to_sec("noncombat idle aiming"),  # seconds
        from_to_sec("noncombat idle looking"),  # seconds
        from_to_sec("guard idle facing"),  # seconds
        from_to_sec("guard idle aiming"),  # seconds
        from_to_sec("guard idle looking"),  # seconds
        from_to_sec("combat idle facing"),  # seconds
        from_to_sec("combat idle aiming"),  # seconds
        from_to_sec("combat idle looking"),  # seconds

        Pad(24),
        dependency("DO NOT USE 1", "weap"),

        Pad(268),
        dependency("DO NOT USE 2", "proj")
        ),

    Struct("unopposable",
        SEnum16("unreachable danger trigger", *danger_triggers),
        SEnum16("vehicle danger trigger", *danger_triggers),
        SEnum16("player danger trigger", *danger_triggers),

        Pad(2),
        from_to_sec("danger trigger time"),  # seconds
        SInt16("friends killed trigger"),
        SInt16("friends retreating trigger"),

        Pad(12),
        from_to_sec("retreat time"),  # seconds
        ),

    Pad(8),
    Struct("panic",
        from_to_sec("cowering time"),  # seconds
        float_zero_to_one("friend killed panic chance"),
        SEnum16("leader type", *actor_types),

        Pad(2),
        float_zero_to_one("leader killed panic chance"),
        float_zero_to_one("panic damage threshold"),
        float_wu("surprise distance"),  # world units
        ),

    Pad(28),
    Struct("defensive",
        from_to_sec("hide behind cover time"),  # seconds
        float_sec("hide target-not-visible time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_zero_to_one("hide shield fraction"),
        float_zero_to_one("attack shield fraction"),
        float_zero_to_one("pursue shield fraction"),

        Pad(16),
        SEnum16("defensive crouch type",
            "never",
            "danger",
            "low shields",
            "hide behind shield",
            "any target",
            "flood shamble"
            ),

        Pad(2),
        Float("attacking crouch threshold"),
        Float("defending crouch threshold"),
        float_sec("mim stand time",  UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("mim crouch time", UNIT_SCALE=sec_unit_scale),  # seconds
        Float("defending hide time modifier"),
        Float("attacking evasion threshold"),
        Float("defending evasion threshold"),
        float_zero_to_one("evasion seek-cover chance"),
        float_sec("evasion delay time", UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("max seek cover distance"),  # world units
        float_zero_to_one("cover damage threshold"),
        float_sec("stalking discovery time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("stalking max distance"),  # world units
        float_rad("stationary facing angle"),  # radians
        float_sec("change facing stand time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        ),

    Pad(4),
    Struct("pursuit",
        from_to_sec("uncover delay time"),  # seconds
        from_to_sec("target search time"),  # seconds
        from_to_sec("pursuit position time"),  # seconds
        SInt16("coordinated position count", MIN=0),
        SInt16("normal position count", MIN=0),
        ),

    Pad(32),
    QStruct("berserk",
        float_sec("melee attack delay", UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("melee fudge factor"),  # world units
        float_sec("melee charge time",  UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("melee leap range lower bound"),  # world units
        float_wu("melee leap range upper bound"),  # world units
        Float("melee leap velocity", SIDETIP="world units/tick",
               UNIT_SCALE=per_sec_unit_scale),  # world units/tick
        float_zero_to_one("melee leap chance"),
        float_zero_to_one("melee leap ballistic"),
        float_zero_to_one("berserk damage amount"),
        float_zero_to_one("berserk damage threshold"),
        float_wu("berserk proximity"),  # world units
        float_wu("suicide sensing dist"),  # world units
        float_zero_to_one("berserk grenade chance"),
        ),

    Pad(12),
    Struct("firing positions",
        from_to_sec("guard position time"),  # seconds
        from_to_sec("combat position time"),  # seconds
        Float("old position avoid dist"),  # world units
        Float("friend avoid dist"),  # world units
        ),

    Pad(40),
    Struct("communication",
        from_to_sec("noncombat idle speech time"),  # seconds
        from_to_sec("combat idle speech time"),  # seconds

        Pad(176),
        dependency("DO NOT USE 3", "actr"),
        ),
    SIZE=1272
    )


def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header('actr', 2),
    actr_body,

    ext=".actor", endian=">", tag_cls=HekTag
    )
