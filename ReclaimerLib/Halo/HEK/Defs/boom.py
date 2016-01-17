from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return BOOM_Def

class BOOM_Def(Tag_Def):

    Ext = ".spheroid"

    Cls_ID = "boom"

    Endian = ">"

    Tag_Structure = { TYPE:Container, GUI_NAME:"spheroid",
                      0:Combine( {1:{ DEFAULT:"boom" } }, Tag_Header),

                      1:{ TYPE:Struct, SIZE:4, GUI_NAME:"Data",
                          #this is just a guess. This could just as easily
                          #be 4 bytes of padding. effing useless tag type
                          0:{TYPE:Float, NAME:'Radius'}
                          }
                      }
