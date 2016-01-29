from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return PphyDef

class PphyDef(TagDef):

    ext = ".point_physics"

    tag_id = "pphy"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"point_physics",
                     0:com( {1:{ DEFAULT:"pphy" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:64, GUI_NAME:"Data",
                        0:{ TYPE:Bool32, OFFSET:0, GUI_NAME:"Flags",
                            0:{GUI_NAME:"Flamethrower particle collision"},
                            1:{GUI_NAME:"Collides with structures"},
                            2:{GUI_NAME:"Collides with water surface"},
                            3:{GUI_NAME:"Uses simple wind"},
                            4:{GUI_NAME:"Uses damped wind"},
                            5:{GUI_NAME:"No gravity"}
                            },
                        #these next three are courtesy of Sparky. I had
                        #no idea these existed till I looked in Eschaton
                        1:{ TYPE:FlFloat, OFFSET:4, GUI_NAME:"Wind Coefficient" },
                        2:{ TYPE:FlFloat, OFFSET:8, GUI_NAME:"Wind Sine Modifier" },
                        3:{ TYPE:FlFloat, OFFSET:12, GUI_NAME:"Z Translation Rate" },
                        
                        4:{ TYPE:Float, OFFSET:32, GUI_NAME:"Density"},#g/mL
                        5:{ TYPE:Float, OFFSET:36, GUI_NAME:"Air Friction" },
                        6:{ TYPE:Float, OFFSET:40, GUI_NAME:"Water Friction" },
                        7:{ TYPE:Float, OFFSET:44, GUI_NAME:"Surface Friction" },
                        8:{ TYPE:Float, OFFSET:48, GUI_NAME:"Elasticity" },
                        }
                     }
