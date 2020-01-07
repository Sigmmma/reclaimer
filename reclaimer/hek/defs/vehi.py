#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .unit import *
from .objs.obje import ObjeTag

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=1)

vehi_attrs = Struct("vehi_attrs",
    Bool32("flags",
        "speed_wakes_physics",
        "turn_wakes_physics",
        "driver_power_wakes_physics",
        "gunner_power_wakes_physics",
        "control_opposite_sets_brake",
        "slide_wakes_physics",
        "kills_riders_at_terminal_velocity",
        "causes_collision_damage",
        "ai_weapon_cannot_rotate",
        "ai_does_not_require_driver",
        "ai_unused",
        "ai_driver_enable",
        "ai_driver_flying",
        "ai_driver_can_sidestep",
        "ai_driver_hovering",
        ),
    SEnum16('type', *vehicle_types),

    Pad(2),
    float_wu_sec("maximum_forward_speed"),
    float_wu_sec("maximum_reverse_speed"),
    float_wu_sec_sq("speed_acceleration", UNIT_SCALE=per_sec_unit_scale),
    float_wu_sec_sq("speed_deceleration", UNIT_SCALE=per_sec_unit_scale),
    Float("maximum_left_turn"),
    Float("maximum_right_turn", SIDETIP="(should be negative)"),
    float_wu("wheel_circumference"),  # world units
    Float("turn_rate",  UNIT_SCALE=per_sec_unit_scale),
    Float("blur_speed", UNIT_SCALE=per_sec_unit_scale),
    SEnum16('A_in', *vehicle_inputs),
    SEnum16('B_in', *vehicle_inputs),
    SEnum16('C_in', *vehicle_inputs),
    SEnum16('D_in', *vehicle_inputs),

    Pad(12),
    Float("maximum_left_slide"),
    Float("maximum_right_slide"),
    Float("slide_acceleration", UNIT_SCALE=per_sec_unit_scale),
    Float("slide_deceleration", UNIT_SCALE=per_sec_unit_scale),
    Float("minimum_flipping_angular_velocity", UNIT_SCALE=per_sec_unit_scale),
    Float("maximum_flipping_angular_velocity", UNIT_SCALE=per_sec_unit_scale),

    Pad(24),
    float_deg("fixed_gun_yaw"),  # degrees
    float_deg("fixed_gun_pitch"),  # degrees

    Pad(24),
    Struct("ai",
        Float("sidestep_distance"),
        Float("destination_radius"),
        Float("avoidance_distance"),
        Float("pathfinding_radius"),
        float_sec("charge_repeat_timeout"),
        Float("strafing_abort_range"),
        from_to_rad("oversteering_bounds"),  # radians
        float_rad("steering_maximum"),  # radians
        Float("throttle_maximum"),
        float_sec("move_position_time"),
        ),

    Pad(4),
    dependency('suspension_sound', "snd!"),
    dependency('crash_sound', "snd!"),
    dependency('material_effect', "foot"),
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

    ext=".vehicle", endian=">", tag_cls=ObjeTag
    )
