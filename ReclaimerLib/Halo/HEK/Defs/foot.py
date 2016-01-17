from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return FOOT_Def

class FOOT_Def(Tag_Def):

    Ext = ".material_effects"

    Cls_ID = "foot"

    Endian = ">"

    Material = { TYPE:Struct, SIZE:48, NAME:"Material",
                 0:{ TYPE:Tag_Index_Ref, GUI_NAME:"Effect",
                     INCLUDE:Tag_Index_Ref_Struct,
                     },
                 1:{ TYPE:Tag_Index_Ref, GUI_NAME:"Sound",
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

    Tag_Structure = {TYPE:Container, GUI_NAME:"material_effects",
                     0:Combine( {1:{ DEFAULT:"foot" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:140, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Effects",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{ TYPE:Array, GUI_NAME:"Effects Array",
                                     SIZE:".Count", MAX:13, SUB_STRUCT:Effect
                                     }
                             }
                         }
                     }
