from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
                  
item_permutation = Struct("permutation",
    Pad(32),
    BFloat("weight"),
    dependency("item"),
    SIZE=84,
    )

itmc_body = Struct("tagdata",
    reflexive("item permutations", item_permutation, 32767),
    BSInt16("spawn time"),
    SIZE=92,
    )


def get():
    return itmc_def

itmc_def = TagDef("itmc",
    blam_header('itmc',0),
    itmc_body,

    ext=".item_collection", endian=">"
    )
