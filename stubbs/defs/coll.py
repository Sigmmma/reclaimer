from ...hek.defs.coll import *
from ..common_descs import *

shield = dict(shield)
shield[2] = SEnum16("shield material type", *materials_list)

permutation = Struct("permutation",
    ascii_str32("name"),
    ascii_str32("unknown"),
    SIZE=128
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
    Pad(20),
    Float("damage threshold"),
    QStruct("unknown floats", *[Float("float%s" % i) for i in range(11)]),

    dependency_stubbs("destroyed garbage", "garb"),
    dependency_stubbs("destroyed weapon", "weap"),
    dependency_stubbs("destroyed effect", "effe"),
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
    SEnum16("material type", *materials_list),
    Pad(2),
    Float("shield leak percentage"),
    Float("shield damage multiplier"),

    Pad(16+12),
    Float("body damage multiplier"),
    SIZE=144
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

fast_coll_body = dict(coll_body)
fast_coll_body[12] = reflexive("nodes", fast_node, 64, DYN_NAME_PATH='.name')


def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header_stubbs("coll", 11),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=HekTag
    )

fast_coll_def = TagDef("coll",
    blam_header_stubbs("coll", 11),  # bump this up 1 so we can tell it's stubbs
    fast_coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=HekTag,
    )
