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

cdmg_body = dict(cdmg_body)
cdmg_body[5] = dict(cdmg_body[5])
cdmg_body[6] = damage_modifiers
cdmg_body[5][1] = SEnum16("category", *damage_category)
cdmg_body[5][2] = Bool32("flags",
    "does_not_hurt_owner",
    {NAME: "headshot", GUI_NAME: "causes headshots"},
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
     GUI_NAME: "causes multiplayer headshots"},
    "infection_form_pop",
    )

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header_stubbs('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">"
    )
