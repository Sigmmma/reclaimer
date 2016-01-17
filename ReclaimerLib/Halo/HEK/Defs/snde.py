from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return SNDE_Def

class SNDE_Def(Tag_Def):

    Ext = ".sound_environment"

    Cls_ID = "snde"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"sound_environment",
                     0:Combine( {1:{ DEFAULT:"snde" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:72, GUI_NAME:"Data",
                         #I didnt feel like adding offsets since
                         #there is only padding in two spots
                         0:{ TYPE:Pad, SIZE:4 },
                         1:{ TYPE:UInt16, GUI_NAME:"Priority" },
                         2:{ TYPE:Pad, SIZE:2 },
                         3:{ TYPE:Float,  GUI_NAME:"Room Intensity" },
                         4:{ TYPE:Float,  GUI_NAME:"Room Intensity Hf" },
                         5:{ TYPE:Float,  GUI_NAME:"Room Rolloff" },
                         6:{ TYPE:Float,  GUI_NAME:"Decay Time" },
                         7:{ TYPE:Float,  GUI_NAME:"Decay Hf Ratio" },
                         8:{ TYPE:Float,  GUI_NAME:"Reflections Intensity" },
                         9:{ TYPE:Float,  GUI_NAME:"Reflections Delay" },
                         10:{ TYPE:Float,  GUI_NAME:"Reverb Intensity" },
                         11:{ TYPE:Float,  GUI_NAME:"Reverb Delay" },
                         12:{ TYPE:Float, GUI_NAME:"Diffusion" },
                         13:{ TYPE:Float, GUI_NAME:"Density" },
                         14:{ TYPE:Float, GUI_NAME:"Hf Reference" },
                         }
                     }
