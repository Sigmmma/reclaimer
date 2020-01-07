#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .objs.obje import ObjeTag

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

material_response = Struct("material_response",
    Bool16("flags",
        "cannot_be_overpenetrated",
        ),
    SEnum16('response', *responses),
    dependency('effect', "effe"),

    Pad(16),
    Struct("potential_response",
        SEnum16('response', *responses),
        Bool16("flags",
            "only_against_units",
            ),
        float_zero_to_one("skip_fraction"),
        from_to_rad("impact_angle"),  # radians
        from_to_wu_sec("impact_velocity"),  # world units/second
        dependency('effect', "effe"),
        ),

    Pad(16),
    SEnum16("scale_effects_by",
        "damage",
        "angle",
        ),
    Pad(2),
    float_rad("angular_noise"),
    float_wu_sec("velocity_noise"),
    dependency('detonation_effect', "effe"),

    Pad(24),
    # Penetration
    Float("initial_friction", UNIT_SCALE=per_sec_unit_scale),
    Float("maximum_distance"),

    # Reflection
    Float("parallel_refriction",    UNIT_SCALE=per_sec_unit_scale),
    Float("perpendicular_friction", UNIT_SCALE=per_sec_unit_scale),

    SIZE=160
    )

proj_attrs = Struct("proj_attrs",
    Bool32("flags",
        "oriented_along_velocity",
        "ai_must_use_ballistic_aiming",
        "detonation_max_time_if_attached",
        "has_super_combining_explosion",
        "add_parent_velocity_to_initial_velocity",
        "random_attached_detonation_time",
        "minimum_unattached_detonation_time",
        ),
    SEnum16('detonation_timer_starts',
        "immediately",
        "on_first_bounce",
        "when_at_rest",
        ),
    SEnum16('impact_noise', *sound_volumes),
    SEnum16('A_in', *projectile_inputs),
    SEnum16('B_in', *projectile_inputs),
    SEnum16('C_in', *projectile_inputs),
    SEnum16('D_in', *projectile_inputs),
    dependency('super_detonation', "effe"),
    float_wu("ai_perception_radius"),
    float_wu("collision_radius"),

    Struct("detonation",
        float_sec("arming_time"),
        float_wu("danger_radius"),
        dependency('effect', "effe"),
        from_to_sec("timer"),
        float_wu_sec("minimum_velocity"),
        float_wu("maximum_range"),
        ),

    Struct("physics",
        Float("air_gravity_scale"),
        from_to_wu("air_damage_range"),
        Float("water_gravity_scale"),
        from_to_wu("water_damage_range"),
        float_wu_sec("initial_velocity"),  # world units/sec
        float_wu_sec("final_velocity"),  # world units/sec
        float_rad_sec("guided_angular_velocity"),  # radians/second
        SEnum16('detonation_noise', *sound_volumes),

        Pad(2),
        dependency('detonation_started', "effe"),
        dependency('flyby_sound', "snd!"),
        dependency('attached_detonation_damage', "jpt!"),
        dependency('impact_damage', "jpt!"),
        ),

    Pad(12),
    reflexive("material_responses", material_response,
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

    ext=".projectile", endian=">", tag_cls=ObjeTag
    )
