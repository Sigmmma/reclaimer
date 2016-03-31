from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return TagcDef

class TagcDef(TagDef):

    ext = ".tag_collection"

    def_id = "tagc"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"tag_collection",
                     0:com( {1:{ DEFAULT:"tagc" } }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Tag References",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{TYPE:Array, GUI_NAME:"Tag References Array",
                                    SIZE:".Count", MAX:200,
                                    SUB_STRUCT:{ TYPE:TagIndexRef,
                                                 SIZE:16, GUI_NAME:"Tag",
                                                 INCLUDE:Tag_Index_Ref_Struct,
                                                 }
                                    }
                             }
                         }
                     }
