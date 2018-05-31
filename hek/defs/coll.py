from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

body = Struct("body",
    Float("maximum body vitality"),
    Float("body system shock"),

    Pad(52),
    float_zero_to_one("friendly damage resistance"),

    Pad(40),
    dependency("localized damage effect", "effe"),

    float_zero_to_one("area damage effect threshold"),
    dependency("area damage effect", "effe"),

    Float("body damaged threshold"),
    dependency("body damaged effect", "effe"),
    dependency("body depleted effect", "effe"),
    Float("body destroyed threshold"),
    dependency("body destroyed effect", "effe"),
    )

shield = Struct("shield",
    Float("maximum shield vitality"),

    Pad(2),
    SEnum16("shield material type", *materials_list),

    Pad(24),
    SEnum16("shield failure function", *fade_functions),

    Pad(2),
    Float("shield failure threshold"),
    Float("shield failing leak fraction"),

    Pad(16),
    Float("minimum stun damage"),
    float_sec("stun time"),
    float_sec("recharge time"),

    Pad(112),
    Float("shield damaged threshold"),
    dependency("shield damaged effect", "effe"),
    dependency("shield depleted effect", "effe"),
    dependency("shield recharging effect", "effe"),
    )

bsp3d_node = QStruct("bsp3d node",
    SInt32("plane"),
    SInt32("back child"),
    SInt32("front child"),
    SIZE=12
    )

plane = QStruct("plane",
    # i, j, and k form a unit vector where d(presumably)
    # specifies the location of a point a "distance" along it
    Float("i"), Float("j"), Float("k"), Float("d"),
    SIZE=16, ORIENT='h'
    )

leaf = Struct("leaf",
    Bool16("flags",
        "contains double sided surfaces"
        ),
    SInt16("bsp2d reference count"),
    SInt32("first bsp2d reference"),
    SIZE=8
    )

bsp2d_reference = QStruct("bsp2d reference",
    SInt32("plane"),
    SInt32("bsp2d node"),
    SIZE=8
    )

bsp2d_node = QStruct("bsp2d node",
    Float("plane i"),
    Float("plane j"),
    Float("plane d"),
    SInt32("left child"),
    SInt32("right child"),
    SIZE=20
    )

surface = Struct("surface",
    SInt32("plane"),
    SInt32("first edge"),
    Bool8("flags",
        "two sided",
        "invisible",
        "climbable",
        "breakable",
        ),
    SInt8("breakable surface"),
    SInt16("material"),
    SIZE=12
    )

edge = QStruct("edge",
    SInt32("start vertex"),
    SInt32("end vertex"),
    SInt32("forward edge"),
    SInt32("reverse edge"),
    SInt32("left surface"),
    SInt32("right surface"),
    SIZE=24
    )

vertex = QStruct("vertex",
    Float("x"),
    Float("y"),
    Float("z"),
    SInt32("first edge"),
    SIZE=16
    )

permutation_bsp = Struct("permutation bsp",
    reflexive("bsp3d nodes", bsp3d_node, 131072),
    reflexive("planes", plane, 65535),
    reflexive("leaves", leaf, 65535),
    reflexive("bsp2d references", bsp2d_reference, 131072),
    reflexive("bsp2d nodes", bsp2d_node, 65535),
    reflexive("surfaces", surface, 131072),
    reflexive("edges", edge, 262144),
    reflexive("vertices", vertex, 131072),
    SIZE=96
    )

node = Struct("node",
    ascii_str32("name"),
    dyn_senum16("region",
        DYN_NAME_PATH=".....regions.regions_array[DYN_I].name"),
    dyn_senum16("parent node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("next sibling node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first child node",
        DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    FlSInt16("unknown0", VISIBLE=False),
    FlSInt16("unknown1", VISIBLE=False),
    reflexive("bsps", permutation_bsp, 32),
    SIZE=64
    )

pathfinding_sphere = Struct("pathfinding sphere",
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
    Float("damage threshold"),

    Pad(12),
    dependency("destroyed effect", "effe"),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH='.name'),
    SIZE=84
    )

material = Struct("material",
    ascii_str32("name"),
    Bool32("flags",
        "head"
        ),
    SEnum16("material type", *materials_list),
    Pad(2),
    Float("shield leak percentage"),
    Float("shield damage multiplier"),

    Pad(12),
    Float("body damage multiplier"),
    SIZE=72
    )

coll_body = Struct("tagdata",
    Bool32("flags",
        "takes shield damage for children",
        "takes body damage for children",
        "always shields friendly damage",
        "passes area damage to children",
        "parent never takes body damage for us",
        "only damaged by explosives",
        "only damaged while occupied",
        ),
    dyn_senum16("indirect damage material",
        DYN_NAME_PATH=".materials.materials_array[DYN_I].name"),
    Pad(2),

    body,
    shield,

    Pad(124),
    reflexive("materials", material, 32, DYN_NAME_PATH='.name'),
    reflexive("regions", region, 8, DYN_NAME_PATH='.name'),
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
    reflexive("nodes", node, 64, DYN_NAME_PATH='.name'),

    SIZE=664,
    )


fast_collision_bsp = Struct("permutation bsp",
    raw_reflexive("bsp3d nodes", bsp3d_node, 131072),
    raw_reflexive("planes", plane, 65535),
    raw_reflexive("leaves", leaf, 65535),
    raw_reflexive("bsp2d references", bsp2d_reference, 131072),
    raw_reflexive("bsp2d nodes", bsp2d_node, 65535),
    raw_reflexive("surfaces", surface, 131072),
    raw_reflexive("edges", edge, 262144),
    raw_reflexive("vertices", vertex, 131072),
    SIZE=96
    )

fast_node = Struct("node",
    ascii_str32("name"),
    dyn_senum16("region",
        DYN_NAME_PATH=".....regions.regions_array[DYN_I].name"),
    dyn_senum16("parent node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("next sibling node",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first child node",
        DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    FlSInt16("unknown0", VISIBLE=False),
    FlSInt16("unknown1", VISIBLE=False),
    reflexive("bsps", fast_collision_bsp, 32),
    SIZE=64
    )

fast_coll_body = dict(coll_body)
fast_coll_body[12] = reflexive("nodes", fast_node, 64, DYN_NAME_PATH='.name')


def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header("coll", 10),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=HekTag,
    )

fast_coll_def = TagDef("coll",
    blam_header("coll", 10),
    fast_coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=HekTag,
    )
