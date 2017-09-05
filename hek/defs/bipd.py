'''
Names for the "physics" struct in the biped tag are courtesy of Sparky.
The source files where the information was taken from are here:

https://github.com/LiquidLightning/infernal/blob/master/infernal/inf_bipd.h
'''
from math import sqrt
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
    Float("moving turning speed",
        SIDETIP="degrees/sec", UNIT_SCALE=180/pi),  # radians
    Bool32("flags",
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
    SEnum16('A in', *biped_inputs),
    SEnum16('B in', *biped_inputs),
    SEnum16('C in', *biped_inputs),
    SEnum16('D in', *biped_inputs),
    dependency('DONT USE', "jpt!"),

    ####################################################
    #####                   IMPORTANT              #####
    ##### Because of how halo handles some things, #####
    ##### the below accelerations unit scales for  #####
    ##### 60fps must be cut by 2 rather than 4     #####
    ####################################################
    QStruct("flying",
        float_rad("bank angle"),  # radians
        float_sec("bank apply time", UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("bank decay time", UNIT_SCALE=sec_unit_scale),  # seconds
        Float("pitch ratio"),
        float_wu_sec("max velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("max sidestep velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec_sq("acceleration",
                        UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
        float_wu_sec_sq("deceleration",
                        UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
        float_rad_sec("angular velocity maximum"),  # radians/second
        float_rad_sec_sq("angular acceleration maximum"),  # radians/second^2
        float_zero_to_one("crouch velocity modifier"),
        ),

    Pad(8),
    Struct("movement",
        float_rad("maximum slope angle"),  # radians
        float_rad("downhill falloff angle"),  # radians
        float_rad("downhill cutoff angle"),  # radians
        Float("downhill velocity scale"),
        float_rad("uphill falloff angle"),  # radians
        float_rad("uphill cutoff angle"),  # radians
        Float("uphill velocity scale"),

        Pad(24),
        dependency('footsteps', "foot"),
        ),

    Pad(24),
    QStruct("jumping and landing",
        float_wu_sec("jump velocity", UNIT_SCALE=per_sec_unit_scale),
        Pad(28),
        float_sec("maximum soft landing time", UNIT_SCALE=sec_unit_scale),
        float_sec("maximum hard landing time", UNIT_SCALE=sec_unit_scale),
        float_wu_sec("minimum soft landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("minimum hard landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("maximum hard landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("death hard landing velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        ),

    Pad(20),
    QStruct("camera, collision, and autoaim",
        float_wu("standing camera height"),
        float_wu("crouching camera height"),
        float_sec("crouch transition time", UNIT_SCALE=sec_unit_scale),

        Pad(24),
        float_wu("standing collision height"),
        float_wu("crouching collision height"),
        float_wu("collision radius"),

        Pad(40),
        float_wu("autoaim width"),
        ),

    Pad(108),
    QStruct("physics",
        # the default values below that aren't commented out are taken
        # from the cyborg.biped tag after saving it with guerilla.
        FlFloat("ground camera contact multiplier",  DEFAULT=0.17364822328090668),#DEFAULT=1.0),
        FlFloat("crouch camera velocity multiplier", DEFAULT=1/6),#DEFAULT=1.0),
        FlFloat("ground surface height", DEFAULT=sqrt(2)/2,#DEFAULT=1.0,
                TOOLTIP=("negative is walking on walls.\n > 0.707107 is " +
                         "floating with contact points off the ground")),
        FlFloat("ground accel modifier inverse", DEFAULT=-0.3420201241970062),#DEFAULT=-0.0),
        FlFloat("unknown", TOOLTIP="autoaim related?", DEFAULT=-sqrt(2)/2),#DEFAULT=-0.0),
        FlFloat("ground accel modifier fp", DEFAULT=0.3420201241970062),#DEFAULT=0.0),
        FlFloat("ground accel modifier 3p", DEFAULT=sqrt(2)/2, #DEFAULT=0.0,
                TOOLTIP="does the same thing as the fp accel modifier?"),
        FlSInt32("camera mass", DEFAULT=-1, TOOLTIP="unused?"),
        COMMENT=(
            "\nNames for these values are courtesy of Sparky.\n" +
            "From what I understand though, these names are completely\n" +
            "experimental, so don't trust that they are 100% accurate.\n"
            ),
        VISIBLE=False, SIZE=32
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
