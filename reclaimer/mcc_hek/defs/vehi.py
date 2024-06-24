#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.vehi import *
from .obje import *
from .unit import *
    
vehi_flags = Bool32("flags",
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
    "vehicle_steers_directly",
    "unused",
    "has_e_brake",
    "noncombat_vehicle",
    "no_friction_with_driver",
    "can_trigger_automatic_opening_doors",
    "autoaim_when_teamless"
    )

obje_attrs = obje_attrs_variant(obje_attrs, "vehi")
vehi_attrs = desc_variant(vehi_attrs, vehi_flags)

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
