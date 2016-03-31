from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return MplyDef

class MplyDef(TagDef):

    ext = ".multiplayer_scenario_description"

    def_id = "mply"

    endian = ">"

    Scenario_Description = { TYPE:Struct, SIZE:68, NAME:"Scenario Description",
                             0:{ TYPE:TagIndexRef, GUI_NAME:"Descriptive Bitmap",
                                 INCLUDE:Tag_Index_Ref_Struct,
                                 },
                             1:{ TYPE:TagIndexRef, GUI_NAME:"Displayed Map Name",
                                 INCLUDE:Tag_Index_Ref_Struct,
                                 },
                             2:{ TYPE:StrLatin1, GUI_NAME:"Scenario Tag Directory Path",
                                 SIZE:32 }
                             }

    descriptor = {TYPE:Container, GUI_NAME:"multiplayer_scenario_description",
                     0:com( {1:{ DEFAULT:"mply" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:12, GUI_NAME:"Data",
                         0:{ TYPE:Reflexive, GUI_NAME:"Multiplayer Scenario Descriptions",
                             INCLUDE:Reflexive_Struct,
                             
                             CHILD:{TYPE:Array, GUI_NAME:"Scenario Descriptions Array",
                                    SIZE:".Count", MAX:32,
                                    SUB_STRUCT:Scenario_Description
                                    }
                             }
                         }
                     }
