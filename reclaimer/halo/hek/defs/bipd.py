from .obje import *
from .unit import *

contact_point = Struct("contact point",
    Pad(32),
    ascii_str32('marker name'),
    SIZE=64
    )

bipd_attrs = Struct("bipd attrs",
    BFloat("moving turning speed"),  # radians
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
    BFloat("stationary turning threshold"),  # radians

    Pad(16),
    BSEnum16('A in', *biped_inputs),
    BSEnum16('B in', *biped_inputs),
    BSEnum16('C in', *biped_inputs),
    BSEnum16('D in', *biped_inputs),
    dependency('dont use', valid_damage_effects),

    QStruct("flying",
        BFloat("bank angle"),  # radians
        BFloat("bank apply time"),
        BFloat("bank decay time"),
        BFloat("pitch ratio"),
        BFloat("max velocity"),  # world units/second
        BFloat("max sidestep velocity"),  # world units/second
        BFloat("acceleration"),  # world units/second^2
        BFloat("deceleration"),  # world units/second^2
        BFloat("angular velocity maximum"),  # radians/second
        BFloat("angular acceleration maximum"),  # radians/second^2
        BFloat("crouch velocity modifier", MIN=0.0, MAX=1.0),
        ),

    Pad(8),
    Struct("movement",
        BFloat("maximum slope angle"),  # radians
        BFloat("downhill falloff angle"),  # radians
        BFloat("downhill cutoff angle"),  # radians
        BFloat("downhill velocity scale"),
        BFloat("uphill falloff angle"),  # radians
        BFloat("uphill cutoff angle"),  # radians
        BFloat("uphill velocity scale"),

        Pad(24),
        dependency('footsteps', valid_material_effects),
        ),

    Pad(24),
    QStruct("jumping and landing",
        BFloat("jump velocity"),
        Pad(28),
        BFloat("maximum soft landing time"),
        BFloat("maximum hard landing time"),
        BFloat("minimum soft landing velocity"),  # world units/second
        BFloat("minimum hard landing velocity"),  # world units/second
        BFloat("maximum hard landing velocity"),  # world units/second
        BFloat("death hard landing velocity"),  # world units/second
        ),

    Pad(20),
    QStruct("camera, collision, and autoaim",
        BFloat("standing camera height"),
        BFloat("crouching camera height"),
        BFloat("crouch transition time"),

        Pad(24),
        BFloat("standing collision height"),
        BFloat("crouching collision height"),
        BFloat("collision radius"),

        Pad(40),
        BFloat("autoaim width"),
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

    reflexive("contact points", contact_point, 2),
    
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

    ext=".biped", endian=">"
    )
