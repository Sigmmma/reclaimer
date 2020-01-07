#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.jpt_ import *
from ..common_descs import *

jpt__body = dict(jpt__body)
jpt__body[16] = dict(jpt__body[16])
jpt__body[17] = damage_modifiers

jpt__body[16][1] = SEnum16("category", *damage_category)
jpt__body[16][2] = Bool32("flags",
    "does_not_hurt_owner",
    {NAME: "headshot", GUI_NAME: "causes headshots"},
    "pings_resistant_units",
    "does_not_hurt_friends",
    "does_not_ping_units",
    "detonates_explosives",
    "only_hurts_shields",
    "causes_flaming_death",
    {NAME: "indicator_points_down",
     GUI_NAME: "damage indicators always points down"},
    "skips_shields",
    "only_hurts_one_infection_form",
    {NAME: "multiplayer_headshot",
     GUI_NAME: "causes multiplayer headshots"},
    "infection_form_pop",
    )


def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header_stubbs('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">"
    )
