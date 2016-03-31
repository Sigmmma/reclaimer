from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return ItmcDef

class ItmcDef(TagDef):

    ext = ".item_collection"

    def_id = "itmc"

    endian = ">"
                             
    Permutation = { TYPE:Struct, SIZE:84, NAME:"Permutation",
                    0:{ TYPE:Pad, SIZE:32 },
                    1:{ TYPE:Float, NAME:"Weight" },
                    2:{ TYPE:TagIndexRef, NAME:"Item",
                        INCLUDE:Tag_Index_Ref_Struct,
                        }
                    }

    descriptor = {TYPE:Container, GUI_NAME:"item_collection",
                     0:com( {1:{ DEFAULT:"itmc" },
                                 5:{ DEFAULT:0 } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:92, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Item Permutations",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{ TYPE:Array, GUI_NAME:"Permutations Array",
                                     SIZE:".Count", MAX:32,
                                     SUB_STRUCT:Permutation
                                     }
                             },
                         1:{ TYPE:SInt16, NAME:"Spawn Time" }
                         }
                     }
