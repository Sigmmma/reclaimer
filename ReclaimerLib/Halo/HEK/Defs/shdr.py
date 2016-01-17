from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return SHDR_Def

class SHDR_Def(Tag_Def):

    Ext = ".shader"

    Cls_ID = "shdr"

    Endian = ">"

    Tag_Structure = { TYPE:Container, GUI_NAME:"shader",
                      0:Com( {1:{ DEFAULT:"shdr" } }, Tag_Header),
                     
                      1:{ TYPE:Struct, SIZE:40, GUI_NAME:"Data",
                          #Radiosity Properties
                          0:Radiosity_Block,
                        
                          #Shader Type
                          1:Material_Type,
                          2:Numeric_Shader_ID,
                          3:{ TYPE:Pad, SIZE:2 }
                          }
                      }
