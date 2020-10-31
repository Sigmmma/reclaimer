#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.coll import CollTag
from supyr_struct.defs.tag_def import TagDef

bsp_node_tooltip = (
    "Refers to a leaf node if negative.\n"
    "Add 0x80000000 to get leaf node index."
    )

modifier = Struct("modifier",
    Pad(52),
    )

body = Struct("body",
    Float("maximum_body_vitality"),
    Float("body_system_shock"),

    Pad(52),
    float_zero_to_one("friendly_damage_resistance"),

    Pad(40),
    dependency("localized_damage_effect", "effe"),

    float_zero_to_one("area_damage_effect_threshold"),
    dependency("area_damage_effect", "effe"),

    Float("body_damaged_threshold"),
    dependency("body_damaged_effect", "effe"),
    dependency("body_depleted_effect", "effe"),
    Float("body_destroyed_threshold"),
    dependency("body_destroyed_effect", "effe"),
    )

shield = Struct("shield",
    Float("maximum_shield_vitality"),

    Pad(2),
    SEnum16("shield_material_type", *materials_list),

    Pad(24),
    SEnum16("shield_failure_function", *fade_functions),

    Pad(2),
    Float("shield_failure_threshold"),
    Float("shield_failing_leak_fraction"),

    Pad(16),
    Float("minimum_stun_damage"),
    float_sec("stun_time"),
    float_sec("recharge_time"),

    Pad(112),
    Float("shield_damaged_threshold"),
    dependency("shield_damaged_effect", "effe"),
    dependency("shield_depleted_effect", "effe"),
    dependency("shield_recharging_effect", "effe"),
    Pad(8),
    Float("shield_recharge_rate", VISIBLE=False),
    )

bsp3d_node = QStruct("bsp3d_node",
    SInt32("plane"),
    SInt32("back_child", TOOLTIP=bsp_node_tooltip),
    SInt32("front_child", TOOLTIP=bsp_node_tooltip),
    SIZE=12
    )

plane = QStruct("plane",
    # i, j, and k form a unit vector where d specifies
    # the location of a point a "distance" along it
    Float("i"), Float("j"), Float("k"), Float("d"),
    SIZE=16, ORIENT='h'
    )

leaf = Struct("leaf",
    Bool16("flags",
        "contains_double_sided_surfaces"
        ),
    SInt16("bsp2d_reference_count"),
    SInt32("first_bsp2d_reference"),
    SIZE=8
    )

bsp2d_reference = QStruct("bsp2d_reference",
    SInt32("plane"),
    SInt32("bsp2d_node", TOOLTIP=bsp_node_tooltip),
    SIZE=8
    )

bsp2d_node = QStruct("bsp2d_node",
    Float("plane_i"),
    Float("plane_j"),
    Float("plane_d"),
    SInt32("left_child", TOOLTIP=bsp_node_tooltip),
    SInt32("right_child", TOOLTIP=bsp_node_tooltip),
    SIZE=20
    )

surface = Struct("surface",
    SInt32("plane"),
    SInt32("first_edge"),
    Bool8("flags",
        "two_sided",
        "invisible",
        "climbable",
        "breakable",
        ),
    SInt8("breakable_surface"),
    SInt16("material"),
    SIZE=12
    )

edge = QStruct("edge",
    SInt32("start_vertex"),
    SInt32("end_vertex"),
    SInt32("forward_edge"),
    SInt32("reverse_edge"),
    SInt32("left_surface"),
    SInt32("right_surface"),
    SIZE=24
    )

vertex = QStruct("vertex",
    Float("x"),
    Float("y"),
    Float("z"),
    SInt32("first_edge"),
    SIZE=16
    )

permutation_bsp = Struct("permutation_bsp",
    reflexive("bsp3d_nodes", bsp3d_node, 131072),
    reflexive("planes", plane, 65535),
    reflexive("leaves", leaf, 65535),
    reflexive("bsp2d_references", bsp2d_reference, 131072),
    reflexive("bsp2d_nodes", bsp2d_node, 65535),
    reflexive("surfaces", surface, 131072),
    reflexive("edges", edge, 262144),
    reflexive("vertices", vertex, 131072),
    SIZE=96
    )

node = Struct("node",
    ascii_str32("name"),
    dyn_senum16("region",
        DYN_NAME_PATH=".....regions.regions_array[DYN_I].name"),
    dyn_senum16("parent_node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("next_sibling_node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first_child_node",
        DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    FlSInt16("unknown0", VISIBLE=False),
    FlSInt16("unknown1", VISIBLE=False),
    reflexive("bsps", permutation_bsp, 32),
    SIZE=64
    )

pathfinding_sphere = Struct("pathfinding_sphere",
    dyn_senum16("node",
        DYN_NAME_PATH=".....nodes.nodes_array[DYN_I].name"),

    Pad(14),
    QStruct("center", INCLUDE=xyz_float),
    Float("radius"),
    SIZE=32
    )

permutation = Struct("permutation",
    ascii_str32("name"),
    SIZE=32
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
        "inhibits_weapon_attack",
        "inhibits_walking",
        "forces_drop_weapon",
        "causes_head_maimed_scream",
        ),
    Pad(4),
    Float("damage_threshold"),

    Pad(12),
    dependency("destroyed_effect", "effe"),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH='.name'),
    SIZE=84
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

    Pad(12),
    Float("body_damage_multiplier"),
    SIZE=72
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


fast_permutation_bsp = Struct("permutation_bsp",
    raw_reflexive("bsp3d_nodes", bsp3d_node, 131072),
    raw_reflexive("planes", plane, 65535),
    raw_reflexive("leaves", leaf, 65535),
    raw_reflexive("bsp2d_references", bsp2d_reference, 131072),
    raw_reflexive("bsp2d_nodes", bsp2d_node, 65535),
    raw_reflexive("surfaces", surface, 131072),
    raw_reflexive("edges", edge, 262144),
    raw_reflexive("vertices", vertex, 131072),
    SIZE=96
    )

fast_node = Struct("node",
    ascii_str32("name"),
    dyn_senum16("region",
        DYN_NAME_PATH=".....regions.regions_array[DYN_I].name"),
    dyn_senum16("parent_node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("next_sibling_node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first_child_node",
        DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    FlSInt16("unknown0", VISIBLE=False),
    FlSInt16("unknown1", VISIBLE=False),
    reflexive("bsps", fast_permutation_bsp, 32),
    SIZE=64
    )

fast_coll_body = dict(coll_body)
fast_coll_body[12] = reflexive("nodes", fast_node, 64, DYN_NAME_PATH='.name')


def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header("coll", 10),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=CollTag,
    )

fast_coll_def = TagDef("coll",
    blam_header("coll", 10),
    fast_coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=CollTag,
    )
