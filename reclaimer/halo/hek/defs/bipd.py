from .objs.tag import HekTag
from .obje import *
from .unit import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=0)

contact_point = Struct("contact point",
    Pad(32),
    ascii_str32('marker name'),
    SIZE=64
    )

bipd_attrs = Struct("bipd attrs",
    BFloat("moving turning speed",
        SIDETIP="degrees/sec", UNIT_SCALE=180/pi),  # radians
    BBool32("flags",
        "turns without aiming",
        "uses player physics",
        "physics pill centered at origin",
        "spherical",
        "passes through other bipeds",
        "can climb any surface",
        "immune to falling damage",
        "rotate while airborne",
        "uses limp body physics",
        "has no dying airborne",
        "random speed increase",
        "uses old player physics",
        ),
    float_rad("stationary turning threshold"),  # radians

    Pad(16),
    BSEnum16('A in', *biped_inputs),
    BSEnum16('B in', *biped_inputs),
    BSEnum16('C in', *biped_inputs),
    BSEnum16('D in', *biped_inputs),
    dependency('DONT USE', "jpt!"),

    QStruct("flying",
        float_rad("bank angle"),  # radians
        float_sec("bank apply time"),
        float_sec("bank decay time"),
        BFloat("pitch ratio"),
        float_wu_sec("max velocity"),  # world units/second
        float_wu_sec("max sidestep velocity"),  # world units/second
        float_wu_sec_sq("acceleration"),  # world units/second^2
        float_wu_sec_sq("deceleration"),  # world units/second^2
        BFloat("angular velocity maximum",  # radians/second
            SIDETIP="degrees/sec", UNIT_SCALE=180/pi),
        BFloat("angular acceleration maximum",  # radians/second^2
            SIDETIP="degrees/(sec^2)", UNIT_SCALE=180/pi),
        float_zero_to_one("crouch velocity modifier"),
        ),

    Pad(8),
    Struct("movement",
        float_rad("maximum slope angle"),  # radians
        float_rad("downhill falloff angle"),  # radians
        float_rad("downhill cutoff angle"),  # radians
        BFloat("downhill velocity scale"),
        float_rad("uphill falloff angle"),  # radians
        float_rad("uphill cutoff angle"),  # radians
        BFloat("uphill velocity scale"),

        Pad(24),
        dependency('footsteps', "foot"),
        ),

    Pad(24),
    QStruct("jumping and landing",
        float_wu_sec("jump velocity"),
        Pad(28),
        float_sec("maximum soft landing time"),
        float_sec("maximum hard landing time"),
        float_wu_sec("minimum soft landing velocity"),  # world units/second
        float_wu_sec("minimum hard landing velocity"),  # world units/second
        float_wu_sec("maximum hard landing velocity"),  # world units/second
        float_wu_sec("death hard landing velocity"),  # world units/second
        ),

    Pad(20),
    QStruct("camera, collision, and autoaim",
        float_wu("standing camera height"),
        float_wu("crouching camera height"),
        float_sec("crouch transition time"),

        Pad(24),
        float_wu("standing collision height"),
        float_wu("crouching collision height"),
        float_wu("collision radius"),

        Pad(40),
        float_wu("autoaim width"),
        ),

    Pad(108),
    QStruct("unknown struct",
        FlFloat("unknown1", DEFAULT=1.0),
        FlFloat("unknown2", DEFAULT=1.0),
        FlFloat("unknown3", DEFAULT=1.0),
        FlFloat("unknown4", DEFAULT=-0.0),
        FlFloat("unknown5", DEFAULT=-0.0),
        FlFloat("unknown6", DEFAULT=0.0),
        FlFloat("unknown7", DEFAULT=0.0),
        FlSInt32("unknown8", DEFAULT=-1),
        ENDIAN='<'
        ),

    reflexive("contact points", contact_point, 2,
        DYN_NAME_PATH='.marker_name'),
    
    SIZE=516
    )

bipd_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    bipd_attrs,
    SIZE=1268,
    )


def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">", tag_cls=HekTag
    )
