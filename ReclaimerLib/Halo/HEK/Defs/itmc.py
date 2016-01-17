from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return ITMC_Def

class ITMC_Def(Tag_Def):

    Ext = ".item_collection"

    Cls_ID = "itmc"

    Endian = ">"
                             
    Permutation = { TYPE:Struct, SIZE:84, NAME:"Permutation",
                    0:{ TYPE:Pad, SIZE:32 },
                    1:{ TYPE:Float, NAME:"Weight" },
                    2:{ TYPE:Tag_Index_Ref, NAME:"Item",
                        INCLUDE:Tag_Index_Ref_Struct,
                        }
                    }

    Tag_Structure = {TYPE:Container, GUI_NAME:"item_collection",
                     0:Combine( {1:{ DEFAULT:"itmc" },
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
