from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from .objs.scex import ScexTag

def get():
    return ScexDef

class ScexDef(TagDef):

    ext = ".shader_transparent_chicago_extended"

    def_id = "scex"

    tag_cls = ScexTag

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"shader_transparent_chicago_extended",
                     0:com( {1:{ DEFAULT:"scex" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:120, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader Type
                        1:Material_Type,
                        2:Numeric_Shader_ID,
                        3:{ TYPE:SInt32, OFFSET:37, GUI_NAME:"Numeric Counter Limit"},#[0,255]
                        
                        # Shader Properties
                        4:com({ TYPE:Bool8, OFFSET:41, GUI_NAME:"Chicago Shader Flags"},
                              Transparent_Shader_Properties),
                        5:com({ TYPE:Enum16, OFFSET:42, GUI_NAME:"First Map Type"},
                              Transparent_Shader_First_Map_Type),
                        6:com({ TYPE:Enum16, OFFSET:44, GUI_NAME:"Framebuffer Blend Function"},
                              Framebuffer_Blend_Modes),
                        7:com({ TYPE:Enum16, OFFSET:46, GUI_NAME:"Framebuffer Fade Mode"},
                              Transparent_Shader_Fade_Mode),
                        8:com({ TYPE:Enum16, OFFSET:48, GUI_NAME:"Framebuffer Fade Source"},
                              Function_Outputs),
                        
                        #Lens Flare
                        9:{ TYPE:Float, OFFSET:52, GUI_NAME:"Lens Flare Spacing"},#world units
                        10:{ TYPE:TagIndexRef, OFFSET:56, GUI_NAME:"Lens Flare" ,
                             INCLUDE:Tag_Index_Ref_Struct
                             },
                        
                        11:{ TYPE:Reflexive, OFFSET:72, GUI_NAME:"Extra Layers",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, NAME:"Extra_Layers_Array",
                                    MAX:4, SIZE:".Count",
                                    SUB_STRUCT:Extra_Layers_Block
                                    }
                             },
                        12:{ TYPE:Reflexive, OFFSET:84, GUI_NAME:"Four Stage Maps",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, NAME:"Four_Stage_Maps_Array",
                                    MAX:4, SIZE:".Count",
                                    SUB_STRUCT:Chicago_4_Stage_Maps
                                    }
                             },
                        13:{ TYPE:Reflexive, OFFSET:96, GUI_NAME:"Two Stage Maps",
                             INCLUDE:Reflexive_Struct,
                             CHILD:{TYPE:Array, NAME:"Two_Stage_Maps_Array",
                                    MAX:2, SIZE:".Count",
                                    SUB_STRUCT:Chicago_2_Stage_Maps
                                    }
                             },
                        14:com({ TYPE:Bool32, OFFSET:108, GUI_NAME:"Extra Flags"},
                                 Chicago_Extra_Flags)
                        }
                     }
