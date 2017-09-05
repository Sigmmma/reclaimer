from .obje import *
from .objs.tag import HekTag

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=5)

responses = (
    "disappear",
    "detonate",
    "reflect",
    "overpenetrate",
    "attach"
    )

material_response = Struct("material response",
    Bool16("flags",
        "cannot be overpenetrated",
        ),
    SEnum16('response', *responses),
    dependency('effect', "effe"),

    Pad(16),
    Struct("potential response",
        SEnum16('response', *responses),
        Bool16("flags",
            "only against units",
            ),
        float_zero_to_one("skip fraction"),
        from_to_rad("impact angle"),  # radians
        from_to_wu_sec("impact velocity"),  # world units/second
        dependency('effect', "effe"),
        ),

    Pad(16),
    SEnum16("scale effects by",
        "damage",
        "angle",
        ),
    Pad(2),
    float_rad("angular noise"),
    float_wu_sec("velocity noise"),
    dependency('detonation effect', "effe"),

    Pad(24),
    # Penetration
    Float("initial friction", UNIT_SCALE=per_sec_unit_scale),
    Float("maximum distance"),

    # Reflection
    Float("parallel refriction",    UNIT_SCALE=per_sec_unit_scale),
    Float("perpendicular friction", UNIT_SCALE=per_sec_unit_scale),

    SIZE=160
    )

proj_attrs = Struct("proj attrs",
    Bool32("flags",
        "oriented along velocity",
        "ai must use ballistic aiming",
        "detonation max time if attached",
        "has super combining explosion",
        "add parent velocity to initial velocity",
        "random attached detonation time",
        "minimum unattached detonation time",
        ),
    SEnum16('detonation timer starts',
        "immediately",
        "on first bounce",
        "when at rest",
        ),
    SEnum16('impact noise', *sound_volumes),
    SEnum16('A in', *projectile_inputs),
    SEnum16('B in', *projectile_inputs),
    SEnum16('C in', *projectile_inputs),
    SEnum16('D in', *projectile_inputs),
    dependency('super detonation', "effe"),
    float_wu("ai perception radius"),
    float_wu("collision radius"),

    Struct("detonation",
        float_sec("arming time"),
        float_wu("danger radius"),
        dependency('effect', "effe"),
        from_to_sec("timer"),
        float_wu_sec("minimum velocity"),
        float_wu("maximum range"),
        ),

    Struct("physics",
        Float("air gravity scale"),
        from_to_wu("air damage range"),
        Float("water gravity scale"),
        from_to_wu("water damage range"),
        float_wu_sec("initial velocity"),  # world units/sec
        float_wu_sec("final velocity"),  # world units/sec
        float_rad_sec("guided angular velocity"),  # radians/second
        SEnum16('detonation noise', *sound_volumes),

        Pad(2),
        dependency('detonation started', "effe"),
        dependency('flyby sound', "snd!"),
        dependency('attached detonation damage', "jpt!"),
        dependency('impact damage', "jpt!"),
        ),

    Pad(12),
    reflexive("material responses", material_response,
        len(materials_list), *materials_list),

    SIZE=208
    )

proj_body = Struct("tagdata",
    obje_attrs,
    proj_attrs,
    SIZE=588,
    )


def get():
    return proj_def

proj_def = TagDef("proj",
    blam_header('proj', 5),
    proj_body,

    ext=".projectile", endian=">", tag_cls=HekTag
    )
