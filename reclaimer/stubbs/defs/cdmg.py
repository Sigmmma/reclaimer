#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.cdmg import *
from ..common_descs import *
from supyr_struct.util import desc_variant

damage = Struct("damage",
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
    )

cdmg_body = desc_variant(cdmg_body,
    ("damage_modifiers", damage_modifiers),
    ("damage", damage)
    )

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header_stubbs('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">"
    )
