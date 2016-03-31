from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return WindDef

class WindDef(TagDef):

    ext = ".wind"

    def_id = "wind"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"wind",
                     0:com( {1:{ DEFAULT:"wind" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:64, GUI_NAME:"Data",
                        #I didnt feel like adding offsets since there is no
                        #padding until AFTER all entries. it's all sequential
                        0:com({ GUI_NAME:"Velocity" }, From_To),
                        1:com({ GUI_NAME:"Variation Area" }, Y_P_Float),
                        2:{ TYPE:Float, GUI_NAME:"Local Variation Weight" },
                        3:{ TYPE:Float, GUI_NAME:"Local Variation Rate" },
                        4:{ TYPE:Float, GUI_NAME:"Damping" }
                        }
                     }
