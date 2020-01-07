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

cdmg_body = Struct("tagdata",
    from_to_wu("radius"),
    float_zero_to_one("cutoff_scale"),
    Pad(24),

    QStruct("vibrate_parameters",
        float_zero_to_one("low_frequency"),
        float_zero_to_one("high_frequency"),
        Pad(24),
        ),

    Struct("camera_shaking",
        float_wu("random_translation"),
        float_rad("random_rotation"),  # radians
        Pad(12),

        SEnum16("wobble_function", *animation_functions),
        Pad(2),
        float_sec("wobble_function_period"),
        Float("wobble_weight"),
        Pad(192),
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
            {NAME: "headshot", GUI_NAME: "can cause headshots"},
            "pings_resistant_units",
            "does_not_hurt_friends",
            "does_not_ping_shields",
            "detonates_explosives",
            "only_hurts_shields",
            "causes_flaming_death",
            {NAME: "indicator_points_down",
             GUI_NAME: "damage indicator always points down"},
            "skips_shields",
            "only_hurts_one_infection_form",
            {NAME: "multiplayer_headshot",
             GUI_NAME: "can cause multiplayer headshots"},
            "infection_form_pop",
            ),
        Pad(4),
        Float("damage_lower_bound"),
        QStruct("damage_upper_bound", INCLUDE=from_to),
        float_zero_to_one("vehicle_passthrough_penalty"),
        Pad(4),
        float_zero_to_one("stun"),
        float_zero_to_one("maximum_stun"),
        float_sec("stun_time"),
        Pad(4),
        float_zero_to_inf("instantaneous_acceleration"),
        Pad(8),
        ),

    damage_modifiers,
    SIZE=512,
    )


def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
