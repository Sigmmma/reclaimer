from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from .Objs.schi import SCHI_Tag

def Construct():
    return SCHI_Def

class SCHI_Def(Tag_Def):

    Ext = ".shader_transparent_chicago"

    Cls_ID = "schi"

    Tag_Cls = SCHI_Tag

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"shader_transparent_chicago",
                     0:Combine( {1:{ DEFAULT:"schi" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:108, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader Type
                        1:Material_Type,
                        2:Numeric_Shader_ID,
                        3:{ TYPE:SInt32, OFFSET:37, GUI_NAME:"Numeric Counter Limit"},#[0,255]
                        
                        # Shader Properties
                        4:Com({ TYPE:Bool8, OFFSET:41, GUI_NAME:"Chicago Shader Flags"},
                              Transparent_Shader_Properties),
                        5:Com({ TYPE:Enum16, OFFSET:42, GUI_NAME:"First Map Type"},
                              Transparent_Shader_First_Map_Type),
                        6:Com({ TYPE:Enum16, OFFSET:44, GUI_NAME:"Framebuffer Blend Function"},
                              Framebuffer_Blend_Modes),
                        7:Com({ TYPE:Enum16, OFFSET:46, GUI_NAME:"Framebuffer Fade Mode"},
                              Transparent_Shader_Fade_Mode),
                        8:Com({ TYPE:Enum16, OFFSET:48, GUI_NAME:"Framebuffer Fade Source"},
                              Function_Outputs),
                        
                        #Lens Flare
                        9:{ TYPE:Float, OFFSET:52, GUI_NAME:"Lens Flare Spacing"},#world units
                        10:{ TYPE:Tag_Index_Ref, OFFSET:56, GUI_NAME:"Lens Flare" ,
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                        
                        11:{ TYPE:Reflexive, OFFSET:72, GUI_NAME:"Extra Layers",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, NAME:"Extra_Layers_Array",
                                    MAX:4, SIZE:".Count",
                                    SUB_STRUCT:Extra_Layers_Block
                                    }
                             },
                        12:{ TYPE:Reflexive, OFFSET:84, GUI_NAME:"Maps",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, NAME:"Maps_Array",
                                    MAX:4, SIZE:".Count",
                                    SUB_STRUCT:Chicago_4_Stage_Maps
                                    }
                             },
                        13:Com({ TYPE:Bool16, OFFSET:98, GUI_NAME:"Extra Flags"},
                               Chicago_Extra_Flags)
                        }
                     }
