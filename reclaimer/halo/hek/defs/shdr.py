from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return ShdrDef

class ShdrDef(TagDef):

    ext = ".shader"

    def_id = "shdr"

    endian = ">"

    descriptor = { TYPE:Container, GUI_NAME:"shader",
                      0:com( {1:{ DEFAULT:"shdr" } }, Tag_Header),
                     
                      1:{ TYPE:Struct, SIZE:40, GUI_NAME:"Data",
                          #Radiosity Properties
                          0:Radiosity_Block,
                        
                          #Shader Type
                          1:Material_Type,
                          2:Numeric_Shader_ID,
                          3:{ TYPE:Pad, SIZE:2 }
                          }
                      }
