from ...hek.defs.coll import *
from ..common_descs import *
from .objs.tag import StubbsTag

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

coll_body = dict(coll_body)
coll_body[4] = dict(coll_body[4])
coll_body[4][2] = BSEnum16("shield material type", *materials_list)
coll_body[6] = reflexive("materials", material, 32, DYN_NAME_PATH='.name')

def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header("coll", 10),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=StubbsTag
    )
