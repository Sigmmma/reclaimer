from .Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from .Objs.scex import SCEX_Tag

def Construct():
    return SCEX_Definition

class SCEX_Definition(Tag_Def):

    Ext = ".shader_transparent_chicago_extended"

    Cls_ID = "scex"

    Tag_Obj = SCEX_Tag

    Endianness = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"shader_transparent_chicago_extended",
                     0:Combine( {1:{ DEFAULT:"scex" } }, Tag_Header),
                     
                     1:{TYPE:Struct, SIZE:120, GUI_NAME:"Data",
                        #Radiosity Properties
                        0:Radiosity_Block,
                        
                        #Shader TYPE
                        1:Material_Type,
                        2:Numeric_Shader_ID,
                        3:{ TYPE:SInt32, OFFSET:37, GUI_NAME:"Numeric Counter Limit"},#[0,255]
                        
                        # Shader Properties
                        4:{ TYPE:UInt8, OFFSET:41, GUI_NAME:"Chicago Shader Flags" ,
                             FLAGS:Transparent_Shader_Properties
                             },
                        5:{ TYPE:UInt16, OFFSET:42, GUI_NAME:"First Map Type" ,
                             ELEMENTS:Transparent_Shader_First_Map_Type
                             },
                        6:{ TYPE:UInt16, OFFSET:44, GUI_NAME:"Framebuffer Blend Function" ,
                             ELEMENTS:Framebuffer_Blend_Modes
                             },
                        7:{ TYPE:UInt16, OFFSET:46, GUI_NAME:"Framebuffer Fade Mode" ,
                             ELEMENTS:Transparent_Shader_Fade_Mode
                             },
                        8:{ TYPE:UInt16, OFFSET:48, GUI_NAME:"Framebuffer Fade Source" ,
                             ELEMENTS:Function_Outputs
                             },
                        
                        #Lens Flare
                        9:{ TYPE:Float, OFFSET:52, GUI_NAME:"Lens Flare Spacing"},#world units
                        10:{ TYPE:Struct, OFFSET:56, GUI_NAME:"Lens Flare" ,
                             ATTRIBUTES:Tag_Reference_Structure
                             },
                        
                        11:{ TYPE:Struct, OFFSET:72, GUI_NAME:"Extra Layers",
                             ATTRIBUTES:Block_Reference_Structure,
                             CHILD:{TYPE:Array, NAME:"Extra_Layers_Array",
                                    MAX:4, SIZE:".Block_Count",
                                    ARRAY_ELEMENT:Extra_Layers_Block
                                    }
                             },
                        12:{ TYPE:Struct, OFFSET:84, GUI_NAME:"Four Stage Maps",
                             ATTRIBUTES:Block_Reference_Structure,
                             CHILD:{TYPE:Array, NAME:"Four_Stage_Maps_Array",
                                    MAX:4, SIZE:".Block_Count",
                                    ARRAY_ELEMENT:Chicago_4_Stage_Maps
                                    }
                             },
                        13:{ TYPE:Struct, OFFSET:96, GUI_NAME:"Two Stage Maps",
                             ATTRIBUTES:Block_Reference_Structure,
                             CHILD:{TYPE:Array, NAME:"Two_Stage_Maps_Array",
                                    MAX:2, SIZE:".Block_Count",
                                    ARRAY_ELEMENT:Chicago_2_Stage_Maps
                                    }
                             },
                        14:{ TYPE:UInt16, OFFSET:110, GUI_NAME:"Extra Flags" ,
                             FLAGS:Chicago_Extra_Flags
                             }
                        }
                     }
