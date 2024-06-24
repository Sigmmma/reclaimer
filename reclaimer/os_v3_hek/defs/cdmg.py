#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.cdmg import *

damage_flags = Bool32("flags",
    "does_not_hurt_owner",
    {NAME: "headshot", GUI_NAME: "can cause headshots"},
    "pings_resistant_units",
    "does_not_hurt_friends",
    "does_not_ping_units",
    "detonates_explosives",
    "only_hurts_shields",
    "causes_flaming_death",
    {NAME: "indicator_points_down", GUI_NAME: "damage indicator always points down"},
    "skips_shields",
    "only_hurts_one_infection_form",
    {NAME: "multiplayer_headshot", GUI_NAME: "can cause multiplayer headshots"},
    "infection_form_pop",
    "YELO_3D_instantaneous_acceleration"
    )

damage = desc_variant(damage,
    damage_flags,
    QStruct("instantaneous_acceleration", INCLUDE=ijk_float, SIDETIP="[-inf,+inf]"),
    ("pad_13", Pad(0)),
    # we're doing some weird stuff to make this work, so we're turning off verify
    verify=False
    )

cdmg_body = desc_variant(cdmg_body, damage)

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
