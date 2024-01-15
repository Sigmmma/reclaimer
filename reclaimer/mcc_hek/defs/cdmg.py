#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.cdmg import *
from supyr_struct.util import desc_variant

damage_flags = Bool32("flags",
    "does_not_hurt_owner",
    {NAME: "headshot", GUI_NAME: "can cause headshots"},
    "pings_resistant_units",
    "does_not_hurt_friends",
    "does_not_ping_shields",
    "detonates_explosives",
    "only_hurts_shields",
    "causes_flaming_death",
    {NAME: "indicator_points_down", GUI_NAME: "damage indicator always points down"},
    "skips_shields",
    "only_hurts_one_infection_form",
    {NAME: "multiplayer_headshot", GUI_NAME: "can cause multiplayer headshots"},
    "infection_form_pop",
    "ignore_seat_scale_for_dir_dmg",
    "forces_hard_ping",
    "does_not_hurt_players",
    "use_3d_instantaneous_acceleration",
    "allow_any_non_zero_acceleration_value",
    )

damage_descs = [
    desc for desc in cdmg_body.values()
    if isinstance(desc, dict) and desc.get("NAME") == "damage"
    ]
if not damage_descs:
    raise ValueError("Could not locate descriptor 'damage' in cdmg_body")

damage = desc_variant(damage_descs[0],
    ("flags", damage_flags),
    ("instantaneous_acceleration", QStruct("instantaneous_acceleration", INCLUDE=ijk_float)),
    ("pad_3", Pad(0)),
    )

cdmg_body = desc_variant(cdmg_body,
    ("damage", damage),
    )

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
