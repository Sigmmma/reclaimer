from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return SoulDef

class SoulDef(TagDef):

    ext = ".ui_widget_collection"

    def_id = "Soul"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"ui_widget_collection",
                     0:com( {1:{ DEFAULT:"Soul" } }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"UI Widget Definitions",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{TYPE:Array, GUI_NAME:"UI Widget Definitions",
                                    SIZE:".Count", MAX:32,
                                    SUB_STRUCT:{ TYPE:TagIndexRef, SIZE:16,
                                                 GUI_NAME:"UI Widget Definition",
                                                 INCLUDE:Tag_Index_Ref_Struct,
                                                 }
                                    }
                             }
                         }
                     }
