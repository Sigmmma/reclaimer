from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
                  
permutation = Struct("permutation",
    Pad(32),
    BFloat("weight"),
    TagIndexRef("item", INCLUDE=Tag_Index_Ref_Struct),
    SIZE=84,
    )

itmc_body = Struct("Data",
    Reflexive("item permutations",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("permutations array",
            SIZE=".Count", MAX=32,
            SUB_STRUCT=permutation
            ),
        ),
    BSInt16("spawn time"),
    SIZE=92,
    )


def get():
    return itmc_def

itmc_def = TagDef(
    com( {1:{DEFAULT:"itmc" },
          5:{DEFAULT:0}}, Tag_Header),
    itmc_body,
    
    NAME="item_collection",
    
    ext=".item_collection", def_id="itmc", endian=">"
    )
