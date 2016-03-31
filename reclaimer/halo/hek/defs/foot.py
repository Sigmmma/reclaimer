from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return FootDef

class FootDef(TagDef):

    ext = ".material_effects"

    def_id = "foot"

    endian = ">"

    Material = { TYPE:Struct, SIZE:48, NAME:"Material",
                 0:{ TYPE:TagIndexRef, GUI_NAME:"Effect",
                     INCLUDE:Tag_Index_Ref_Struct,
                     },
                 1:{ TYPE:TagIndexRef, GUI_NAME:"Sound",
                     INCLUDE:Tag_Index_Ref_Struct,
                     }
                 }
                             
    Effect = { TYPE:Struct, SIZE:28, GUI_NAME:"Effect",
               0:{ TYPE:Reflexive, GUI_NAME:"Materials",
                   INCLUDE:Reflexive_Struct,
                 
                   CHILD:{ TYPE:Array, GUI_NAME:"Materials Array",
                           SIZE:".Count", MAX:33, SUB_STRUCT:Material
                           }
                   }
               }

    descriptor = {TYPE:Container, GUI_NAME:"material_effects",
                     0:com( {1:{ DEFAULT:"foot" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:140, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Effects",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{ TYPE:Array, GUI_NAME:"Effects Array",
                                     SIZE:".Count", MAX:13, SUB_STRUCT:Effect
                                     }
                             }
                         }
                     }
