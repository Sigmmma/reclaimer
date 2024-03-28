#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.weap import *
from .obje import *
from .item import *

trigger_flags = Bool32("flags",
    "tracks_fired_projectile",
    "random_firing_effects",
    "can_fire_with_partial_ammo",
    "does_not_repeat_automatically",
    "locks_in_on_off_state",
    "projectiles_use_weapon_origin",
    "sticks_when_dropped",
    "ejects_during_chamber",
    "discharging_spews",
    "analog_rate_of_fire",
    "use_error_when_unzoomed",
    "projectile_vector_cannot_be_adjusted",
    "projectiles_have_identical_error",
    "projectile_is_client_side_only",
    "use_unit_adjust_projectile_ray_from_halo1",
    )
mcc_upgrades = Struct("mcc_upgrades",
    Pad(4),
    SEnum16("prediction_type",
        'none',
        'continuous',
        'instant',
        ),
    SIZE=6
    )

firing = desc_variant(firing,
    ("pad_9", mcc_upgrades)
    )
trigger = desc_variant(trigger, trigger_flags, firing)

obje_attrs = obje_attrs_variant(obje_attrs, "weap")
weap_attrs = desc_variant(weap_attrs,
    reflexive("triggers", trigger, 2, "primary", "secondary"),
    SEnum16('weapon_type', *weapon_types_mcc)
    )

weap_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    weap_attrs,
    SIZE=1288,
    )


def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">", tag_cls=WeapTag
    )
