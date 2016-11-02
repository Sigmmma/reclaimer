from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

bsp3d_node = QStruct("bsp3d node",
    BSInt32("plane"),
    BSInt32("back child"),
    BSInt32("front child"),
    SIZE=12
    )

plane = QStruct("plane",
    # i, j, and k form a unit vector where d(presumably)
    # specifies the location of a point a "distance" along it
    BFloat("i"),
    BFloat("j"),
    BFloat("k"),
    BFloat("d"),
    SIZE=16
    )

leaf = Struct("leaf",
    Pad(1),
    SInt8("flags",
        "contains double sided surfaces"
        ),
    BSInt16("bsp2d reference count"),
    BSInt32("first bsp2d reference"),
    SIZE=8
    )

bsp2d_reference = QStruct("bsp2d reference",
    BSInt32("plane"),
    BSInt32("bsp2d node"),
    SIZE=8
    )

bsp2d_node = QStruct("bsp2d node",
    BFloat("plane i"),
    BFloat("plane j"),
    BFloat("plane d"),
    BSInt32("left child"),
    BSInt32("right child"),
    SIZE=20
    )

surface = Struct("surface",
    BSInt32("plane"),
    BSInt32("first edge"),
    SInt8("flags",
        "two sided"
        "invisible"
        "climbable"
        "breakable"
        ),
    SInt8("breakable surface"),
    BSInt16("material"),
    SIZE=12
    )

edge = QStruct("edge",
    BSInt32("start vertex"),
    BSInt32("end vertex"),
    BSInt32("forward edge"),
    BSInt32("reverse edge"),
    BSInt32("left surface"),
    BSInt32("right surface"),
    SIZE=24
    )

vertex = QStruct("vertex",
    BFloat("x"),
    BFloat("y"),
    BFloat("z"),
    BSInt32("first edge"),
    SIZE=16
    )

bsp = Struct("bsp",
    reflexive("bsp3d nodes", bsp3d_node),
    reflexive("planes", plane),
    reflexive("leaves", leaf),
    reflexive("bsp2d references", bsp2d_reference),
    reflexive("bsp2d nodes", bsp2d_node),
    reflexive("surfaces", surface),
    reflexive("edges", edge),
    reflexive("vertices", vertex),
    SIZE=96
    )

node = Struct("node",
    ascii_str32("name"),
    BSInt16("region"),
    BSInt16("parent node"),
    BSInt16("next sibling node"),
    BSInt16("first child node"),

    Pad(12),
    reflexive("bsps", bsp, 32),
    SIZE=64
    )

pathfinding_sphere = Struct("pathfinding sphere",
    BSInt16("node"),

    Pad(14),
    QStruct("center", INCLUDE=xyz_float),
    BFloat("radius"),
    SIZE=32
    )

permutation = Struct("permutation",
    ascii_str32("name"),
    SIZE=32
    )

region = Struct("region",
    ascii_str32("name"),
    BBool32("flags",
        "lives until object dies",
        "forces object to die",
        "dies when object dies",
        "dies when object is damaged",
        "disappears when shield is off",
        "inhibits melee attack",
        "inhibits walking",
        "forces drop weapon",
        "causes head-maimed scream",
        ),
    Pad(4),
    BFloat("damage threshold"),

    Pad(12),
    dependency("destroyed effect", valid_effects),
    reflexive("permutations", permutation, 32),
    SIZE=84
    )

material = Struct("material",
    ascii_str32("name"),
    BBool32("flags",
        "head"
        ),
    BSEnum16("material type", *materials_list),
    Pad(2),
    BFloat("shield leak percentage"),
    BFloat("shield damage multiplier"),

    Pad(12),
    BFloat("body damage multiplier"),
    SIZE=72
    )

coll_body = Struct("tagdata",
    BBool32("flags",
        "takes shield damage for children",
        "takes body damage for children",
        "always shields friendly damage",
        "passes area damage to children",
        "parent never takes body damage for us",
        "only damaged by explosives",
        "only damaged while occupied",
        ),
    BSInt16("indirect damage material"),
    Pad(2),

    Struct("body",
        BFloat("maximum body vitality"),
        BFloat("body system shock"),

        Pad(52),
        BFloat("friendly damage resistance", MIN=0.0, MAX=1.0),

        Pad(40),
        dependency("localized damage effect", valid_effects),

        BFloat("area damage effect threshold", MIN=0.0, MAX=1.0),
        dependency("area damage effect", valid_effects),

        BFloat("body damaged threshold"),
        dependency("body damaged effect", valid_effects),
        dependency("body depleted effect", valid_effects),
        BFloat("body destroyed threshold"),
        dependency("body destroyed effect", valid_effects),
        ),

    Struct("shield",
        BFloat("maximum shield vitality"),

        Pad(2),
        BSEnum16("shield material type", *materials_list),

        Pad(24),
        BSEnum16("shield failure function", *fade_functions),

        Pad(2),
        BFloat("shield failure threshold"),
        BFloat("shield failing leak fraction"),

        Pad(16),
        BFloat("minimum stun damage"),
        BFloat("stun time"),
        BFloat("recharge time"),

        Pad(112),
        BFloat("shield damaged threshold"),
        dependency("shield damaged effect", valid_effects),
        dependency("shield depleted effect", valid_effects),
        dependency("shield recharging effect", valid_effects),
        ),

    Pad(124),
    reflexive("materials", material, 32),
    reflexive("regions", region, 8),
    # this reflexive is literally not allowed to have even a single
    # entry in guerilla, so im just gonna replace it with padding.
    Pad(12),
    #reflexive("modifiers", modifier, 0),

    Pad(16),
    Struct("pathfinding box",
        QStruct("x", INCLUDE=from_to),
        QStruct("y", INCLUDE=from_to),
        QStruct("z", INCLUDE=from_to),
        ),

    reflexive("pathfinding spheres", pathfinding_sphere, 32),
    reflexive("nodes", node, 64),

    SIZE=664,
    )


def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header("coll", 10),
    coll_body,

    ext=".model_collision_geometry", endian=">",
    )
