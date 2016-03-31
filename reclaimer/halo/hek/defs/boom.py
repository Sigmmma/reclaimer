from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return BoomDef

class BoomDef(TagDef):

    ext = ".spheroid"

    def_id = "boom"

    endian = ">"

    descriptor = { TYPE:Container, GUI_NAME:"spheroid",
                      0:com( {1:{ DEFAULT:"boom" } }, Tag_Header),

                      1:{ TYPE:Struct, SIZE:4, GUI_NAME:"Data",
                          #this is just a guess. This could just as easily
                          #be 4 bytes of padding. effing useless tag type
                          0:{TYPE:Float, NAME:'Radius'}
                          }
                      }
