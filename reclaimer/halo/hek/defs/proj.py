from .obje import *
from .item import *

responses = (
    "disappear",
    "detonate",
    "reflect",
    "overpenetrate",
    "attach"
    )

material_response = Struct("material response",
    BBool16("flags",
        "cannot be overpenetrated",
        ),
    BSEnum16('response', *responses),
    dependency('effect', valid_effects),

    Pad(16),
    Struct("potential response",
        BSEnum16('response', *responses),
        BBool16("flags",
            "only against units",
            ),
        BFloat("skip fraction", MIN=0.0, MAX=1.0),
        QStruct("impact angle range", INCLUDE=from_to),  # radians
        QStruct("impact velocity range", INCLUDE=from_to),  # world units/second
        dependency('effect', valid_effects),
        ),

    Pad(16),
    BSEnum16("scale effects by",
        "damage",
        "angle",
        ),
    Pad(2),
    BFloat("angular noise"),
    BFloat("velocity noise"),
    dependency('detonation effect', valid_effects),

    Pad(24),
    # Penetration
    BFloat("initial friction"),
    BFloat("maximum distance"),

    # Reflection
    BFloat("parallel refriction"),
    BFloat("perpendicular friction"),

    SIZE=160
    )

projectile_attrs = Struct("projectile attrs",
    BBool32("flags",
        "oriented along velocity",
        "ai must use ballistic aiming",
        "detonation max time if attached",
        "has super combining explosion",
        "add parent velocity to initial velocity",
        "random attached detonation time",
        "minimum unattached detonation time",
        ),
    BSEnum16('detonation timer starts',
        "immediately",
        "on first bounce",
        "when at rest",
        ),
    BSEnum16('impact noise', *sound_volumes),
    BSEnum16('A in', *projectile_inputs),
    BSEnum16('B in', *projectile_inputs),
    BSEnum16('C in', *projectile_inputs),
    BSEnum16('D in', *projectile_inputs),
    dependency('super detonation', valid_effects),
    BFloat("ai perception radius"),
    BFloat("collision radius"),

    Struct("detonation",
        BFloat("arming time"),
        BFloat("danger radius"),
        dependency('effect', valid_effects),
        QStruct("timer", INCLUDE=from_to),
        BFloat("minimum velocity"),
        BFloat("maximum range"),
        ),

    Struct("physics",
        BFloat("air gravity scale"),
        QStruct("air damage range", INCLUDE=from_to),
        BFloat("water gravity scale"),
        QStruct("water damage range", INCLUDE=from_to),
        BFloat("initial velocity"),
        BFloat("final velocity"),
        BFloat("guided angular velocity"),  # radians per second
        BSEnum16('detonation noise', *sound_volumes),

        Pad(2),
        dependency('detonation started', valid_effects),
        dependency('flyby sound', valid_sounds),
        dependency('attached detonation damage', valid_damage_effects),
        dependency('impact damage', valid_damage_effects),
        ),

    Pad(12),
    reflexive("material responses", material_response,
        len(materials_list), *(mat_name for mat_name in materials_list)),

    SIZE=208
    )

proj_body = Struct("tagdata",
    object_attrs,
    projectile_attrs,
    SIZE=588,
    )


def get():
    return proj_def

proj_def = TagDef("proj",
    blam_header('proj', 5),
    proj_body,

    ext=".projectile", endian=">"
    )
