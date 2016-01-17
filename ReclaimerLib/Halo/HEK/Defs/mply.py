from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return MPLY_Def

class MPLY_Def(Tag_Def):

    Ext = ".multiplayer_scenario_description"

    Cls_ID = "mply"

    Endian = ">"

    Scenario_Description = { TYPE:Struct, SIZE:68, NAME:"Scenario Description",
                             0:{ TYPE:Tag_Index_Ref, GUI_NAME:"Descriptive Bitmap",
                                 INCLUDE:Tag_Index_Ref_Struct,
                                 },
                             1:{ TYPE:Tag_Index_Ref, GUI_NAME:"Displayed Map Name",
                                 INCLUDE:Tag_Index_Ref_Struct,
                                 },
                             2:{ TYPE:Str_Latin1, GUI_NAME:"Scenario Tag Directory Path",
                                 SIZE:32 }
                             }

    Tag_Structure = {TYPE:Container, GUI_NAME:"multiplayer_scenario_description",
                     0:Combine( {1:{ DEFAULT:"mply" } }, Tag_Header),
                     
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
