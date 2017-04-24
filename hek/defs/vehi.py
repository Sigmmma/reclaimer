from .obje import *
from .unit import *
from .objs.tag import HekTag

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=1)

vehi_attrs = Struct("vehi attrs",
    BBool32("flags",
        "speed wakes physics",
        "turn wakes physics",
        "driver power wakes physics",
        "gunner power wakes physics",
        "control opposite sets brake",
        "slide wakes physics",
        "kills riders at terminal velocity",
        "causes collision damage",
        "ai weapon cannot rotate",
        "ai does not require driver",
        "ai unused",
        "ai driver enable",
        "ai driver flying",
        "ai driver can sidestep",
        "ai driver hovering",
        ),
    BSEnum16('type', *vehicle_types),

    ####################################################
    #####                   IMPORTANT              #####
    ##### Because of how halo handles some things, #####
    ##### the below accelerations unit scales for  #####
    ##### 60fps must be cut by 2 rather than 4     #####
    ####################################################
    Pad(2),
    float_wu_sec("maximum forward speed"),
    float_wu_sec("maximum reverse speed"),
    float_wu_sec_sq("speed acceleration", UNIT_SCALE=per_sec_unit_scale),
    float_wu_sec_sq("speed deceleration", UNIT_SCALE=per_sec_unit_scale),
    BFloat("maximum left turn"),
    BFloat("maximum right turn", SIDETIP="(should be negative)"),
    float_wu("wheel circumference"),  # world units
    BFloat("turn rate",  UNIT_SCALE=per_sec_unit_scale),
    BFloat("blur speed", UNIT_SCALE=per_sec_unit_scale),
    BSEnum16('A in', *vehicle_inputs),
    BSEnum16('B in', *vehicle_inputs),
    BSEnum16('C in', *vehicle_inputs),
    BSEnum16('D in', *vehicle_inputs),

    Pad(12),
    BFloat("maximum left slide"),
    BFloat("maximum right slide"),
    BFloat("slide acceleration", UNIT_SCALE=per_sec_unit_scale),
    BFloat("slide deceleration", UNIT_SCALE=per_sec_unit_scale),
    BFloat("minimum flipping angular velocity", UNIT_SCALE=per_sec_unit_scale),
    BFloat("maximum flipping angular velocity", UNIT_SCALE=per_sec_unit_scale),

    Pad(24),
    float_deg("fixed gun yaw"),  # degrees
    float_deg("fixed gun pitch"),  # degrees

    Pad(24),
    Struct("ai",
        BFloat("sidestep distance"),
        BFloat("destination radius"),
        BFloat("avoidance distance"),
        BFloat("pathfinding radius"),
        float_sec("charge repeat timeout"),
        BFloat("strafing abort range"),
        from_to_rad("oversteering bounds"),  # radians
        float_rad("steering maximum"),  # radians
        BFloat("throttle maximum"),
        float_sec("move-position time"),
        ),

    Pad(4),
    dependency('suspension sound', "snd!"),
    dependency('crash sound', "snd!"),
    dependency('material effect', "foot"),
    dependency('effect', "effe"),
    
    SIZE=256
    )

vehi_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    vehi_attrs,
    SIZE=1008,
    )


def get():
    return vehi_def

vehi_def = TagDef("vehi",
    blam_header('vehi'),
    vehi_body,

    ext=".vehicle", endian=">", tag_cls=HekTag
    )
