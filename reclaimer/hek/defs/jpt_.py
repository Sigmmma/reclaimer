#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef


frequency_vibration = Struct("",
    float_zero_to_one("frequency"),
    float_sec("duration"),
    SEnum16("fade_function", *fade_functions),
    )

jpt__body = Struct("tagdata",
    from_to_wu("radius"),
    float_zero_to_one("cutoff_scale"),
    Bool32("flags",
        "dont_scale_by_distance",
        ),
    Pad(20),

    #Screen_Flash
    Struct("screen_flash",
        SEnum16("type",
            "none",
            "lighten",
            "darken",
            "max",
            "min",
            "invert",
            "tint",
            ),
        SEnum16("priority",
            "low",
            "medium",
            "high",
            ),
        Pad(12),

        float_sec("duration"),
        SEnum16("fade_function", *fade_functions),
        Pad(10),

        float_zero_to_one("maximum_intensity"),
        Pad(4),

        QStruct("tint_lower_bound", INCLUDE=argb_float),
        ),

    Struct("low_frequency_vibrate", INCLUDE=frequency_vibration),
    Pad(10),
    Struct("high_frequency_vibrate", INCLUDE=frequency_vibration),
    Pad(30),

    Struct("temporary_camera_impulse",
        float_sec("duration"),
        SEnum16("fade_function", *fade_functions),
        Pad(2),

        float_rad("rotation"),  # radians
        float_wu("pushback"),
        from_to_wu("jitter"),
        Pad(8),
        ),

    float_rad("permanent_camera_impulse_angle"),
    Pad(16),

    Struct("camera_shaking",
        float_sec("duration"),
        SEnum16("fade_function", *fade_functions),
        Pad(2),

        float_wu("random_translation"),
        float_rad("random_rotation"),  # radians
        Pad(12),

        SEnum16("wobble_function", *animation_functions),
        Pad(2),
        float_sec("wobble_function_period"),
        Float("wobble_weight"),
        Pad(32),
        ),

    dependency("sound", "snd!"),
    Pad(112),

    QStruct("breaking_effect",
        float_wu_sec("forward_velocity"),
        float_wu("forward_radius"),
        Float("forward_exponent"),
        Pad(12),

        float_wu_sec("outward_velocity"),
        float_wu("outward_radius"),
        Float("outward_exponent"),
        Pad(12),
        ),

    Struct("damage",
        SEnum16("priority",
            "none",
            "harmless",
            {NAME: "backstab", GUI_NAME: "lethal to the unsuspecting"},
            "emp",
            ),
        SEnum16("category", *damage_category),
        Bool32("flags",
            "does_not_hurt_owner",
            {NAME: "headshot", GUI_NAME: "causes headshots"},
            "pings_resistant_units",
            "does_not_hurt_friends",
            "does_not_ping_units",
            "detonates_explosives",
            "only_hurts_shields",
            "causes_flaming_death",
            {NAME: "indicator_points_down",
             GUI_NAME: "damage indicator always points down"},
            "skips_shields",
            "only_hurts_one_infection_form",
            {NAME: "multiplayer_headshot",
             GUI_NAME: "causes multiplayer headshots"},
            "infection_form_pop",
            ),
        float_wu("aoe_core_radius"),
        Float("damage_lower_bound"),
        QStruct("damage_upper_bound", INCLUDE=from_to),
        float_zero_to_one("vehicle_passthrough_penalty"),
        float_zero_to_one("active_camouflage_damage"),
        float_zero_to_one("stun"),
        float_zero_to_one("maximum_stun"),
        float_sec("stun_time"),
        Pad(4),
        float_zero_to_inf("instantaneous_acceleration"),
        Pad(8),
        ),

    damage_modifiers,
    SIZE=672,
    )


def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">", tag_cls=HekTag,
    )
