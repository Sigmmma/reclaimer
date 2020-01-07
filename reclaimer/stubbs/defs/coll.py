#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.coll import *
from ..common_descs import *

shield = dict(shield)
shield[2] = SEnum16("shield_material_type", *materials_list)

permutation = Struct("permutation",
    ascii_str32("name"),
    ascii_str32("unknown"),
    SIZE=128
    )

region = Struct("region",
    ascii_str32("name"),
    Bool32("flags",
        "lives_until_object_dies",
        "forces_object_to_die",
        "dies_when_object_dies",
        "dies_when_object_is_damaged",
        "disappears_when_shield_is_off",
        "inhibits_melee_attack",
        "inhibits_walking",
        "forces_drop_weapon",
        "causes_head_maimed_scream",
        ),
    Pad(20),
    Float("damage_threshold"),
    QStruct("unknown_floats", *[Float("float%s" % i) for i in range(11)]),

    dependency_stubbs("destroyed_garbage", "garb"),
    dependency_stubbs("destroyed_weapon", "weap"),
    dependency_stubbs("destroyed_effect", "effe"),
    ascii_str32("unknown2"),
    Pad(28),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH='.name'),
    SIZE=224
    )

material = Struct("material",
    ascii_str32("name"),
    Bool32("flags",
        "head"
        ),
    SEnum16("material_type", *materials_list),
    Pad(2),
    Float("shield_leak_percentage"),
    Float("shield_damage_multiplier"),

    Pad(16+12),
    Float("body_damage_multiplier"),
    SIZE=144
    )

coll_body = Struct("tagdata",
    Bool32("flags",
        "takes_shield_damage_for_children",
        "takes_body_damage_for_children",
        "always_shields_friendly_damage",
        "passes_area_damage_to_children",
        "parent_never_takes_body_damage_for_us",
        "only_damaged_by_explosives",
        "only_damaged_while_occupied",
        ),
    dyn_senum16("indirect_damage_material",
        DYN_NAME_PATH=".materials.materials_array[DYN_I].name"),
    Pad(2),

    body,
    shield,

    Pad(112),
    reflexive("materials", material, 32, DYN_NAME_PATH='.name'),
    reflexive("regions", region, 8, DYN_NAME_PATH='.name'),
    reflexive("modifiers", modifier, 0, VISIBLE=False),

    Pad(16),
    Struct("pathfinding_box",
        QStruct("x", INCLUDE=from_to),
        QStruct("y", INCLUDE=from_to),
        QStruct("z", INCLUDE=from_to),
        ),

    reflexive("pathfinding_spheres", pathfinding_sphere, 32),
    reflexive("nodes", node, 64, DYN_NAME_PATH='.name'),

    SIZE=664,
    )

fast_coll_body = dict(coll_body)
fast_coll_body[12] = reflexive("nodes", fast_node, 64, DYN_NAME_PATH='.name')


def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header_stubbs("coll", 11),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=CollTag
    )

fast_coll_def = TagDef("coll",
    blam_header_stubbs("coll", 11),  # bump this up 1 so we can tell it's stubbs
    fast_coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=CollTag
    )
