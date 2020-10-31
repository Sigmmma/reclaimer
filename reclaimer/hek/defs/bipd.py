#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
Names for the "physics" struct in the biped tag are courtesy of Sparky.
The source files where the information was taken from are here:

https://github.com/LiquidLightning/infernal/blob/master/infernal/inf_bipd.h

EDIT: updates physics struct with more accurate names determined by Kavawuvi
'''
from math import sqrt
from .objs.bipd import BipdTag
from .obje import *
from .unit import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=0)

contact_point = Struct("contact_point",
    Pad(32),
    ascii_str32('marker_name'),
    SIZE=64
    )

bipd_attrs = Struct("bipd_attrs",
    Float("moving_turning_speed",
        SIDETIP="degrees/sec", UNIT_SCALE=180/pi),  # radians
    Bool32("flags",
        "turns_without_aiming",
        "uses_player_physics",
        "flying",
        "physics_pill_centered_at_origin",
        "spherical",
        "passes_through_other_bipeds",
        "can_climb_any_surface",
        "immune_to_falling_damage",
        "rotate_while_airborne",
        "uses_limp_body_physics",
        "has_no_dying_airborne",
        "random_speed_increase",
        "uses_old_player_physics",
        ),
    float_rad("stationary_turning_threshold"),  # radians

    Pad(16),
    SEnum16('A_in', *biped_inputs),
    SEnum16('B_in', *biped_inputs),
    SEnum16('C_in', *biped_inputs),
    SEnum16('D_in', *biped_inputs),
    dependency('DONT_USE', "jpt!"),

    QStruct("flying",
        float_rad("bank_angle"),  # radians
        float_sec("bank_apply_time", UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("bank_decay_time", UNIT_SCALE=sec_unit_scale),  # seconds
        Float("pitch_ratio"),
        float_wu_sec("max_velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("max_sidestep_velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec_sq("acceleration",
                        UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
        float_wu_sec_sq("deceleration",
                        UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
        float_rad_sec("angular_velocity_maximum"),  # radians/second
        float_rad_sec_sq("angular_acceleration_maximum"),  # radians/second^2
        float_zero_to_one("crouch_velocity_modifier"),
        ),

    Pad(8),
    Struct("movement",
        float_rad("maximum_slope_angle"),  # radians
        float_rad("downhill_falloff_angle"),  # radians
        float_rad("downhill_cutoff_angle"),  # radians
        Float("downhill_velocity_scale"),
        float_rad("uphill_falloff_angle"),  # radians
        float_rad("uphill_cutoff_angle"),  # radians
        Float("uphill_velocity_scale"),

        Pad(24),
        dependency('footsteps', "foot"),
        ),

    Pad(24),
    QStruct("jumping_and_landing",
        float_wu_sec("jump_velocity", UNIT_SCALE=per_sec_unit_scale),
        Pad(28),
        float_sec("maximum_soft_landing_time", UNIT_SCALE=sec_unit_scale),
        float_sec("maximum_hard_landing_time", UNIT_SCALE=sec_unit_scale),
        float_wu_sec("minimum_soft_landing_velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("minimum_hard_landing_velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("maximum_hard_landing_velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        float_wu_sec("death_hard_landing_velocity",
                     UNIT_SCALE=per_sec_unit_scale),  # world units/second
        ),

    Pad(20),
    QStruct("camera_collision_and_autoaim",
        float_wu("standing_camera_height"),
        float_wu("crouching_camera_height"),
        float_sec("crouch_transition_time", UNIT_SCALE=sec_unit_scale),

        Pad(24),
        float_wu("standing_collision_height"),
        float_wu("crouching_collision_height"),
        float_wu("collision_radius"),

        Pad(40),
        float_wu("autoaim_width"),
        ),

    Pad(108),
    QStruct("physics",
        # the default values below that aren't commented out are taken
        # from the cyborg.biped tag after saving it with guerilla.
        FlFloat("cosine_stationary_turning_threshold"),
        FlFloat("crouch_camera_velocity"),
        FlFloat("cosine_maximum_slope_angle",
            TOOLTIP=("negative is walking on walls.\n > 0.707107 is " +
                     "floating with contact points off the ground")),
        FlFloat("neg_sine_downhill_falloff_angle"),
        FlFloat("neg_sine_downhill_cutoff_angle"),
        FlFloat("sine_uphill_falloff_angle"),
        FlFloat("sine_uphill_cutoff_angle",
            TOOLTIP="does the same thing as the fp accel modifier?"),
        FlSInt16("root_node_index", DEFAULT=-1),
        FlSInt16("head_node_index", DEFAULT=-1),
        VISIBLE=False, SIZE=32
        ),

    reflexive("contact_points", contact_point, 2,
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

    ext=".biped", endian=">", tag_cls=BipdTag
    )
