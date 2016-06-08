from ...common_descriptors import *
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

itmc_def = TagDef(
    blam_header('itmc',0),
    itmc_body,
    
    NAME="item_collection",
    
    ext=".item_collection", def_id="itmc", endian=">"
    )
