from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return DEVC_Def

class DEVC_Def(Tag_Def):

    Ext = ".input_device_defaults"

    Cls_ID = "devc"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"input_device_defaults",
                     0:Combine( {1:{ DEFAULT:"devc" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:44, GUI_NAME:"Data",
                         0:{ TYPE:Enum16, GUI_NAME:"Device Type",
                             0:{ GUI_NAME:"Mouse and keyboard" },
                             1:{ GUI_NAME:"Joysticks/joypads/etc" },
                             2:{ GUI_NAME:"Full profile definition" },
                             },
                         1:{ TYPE:Bool16, GUI_NAME:"Flags",
                             0:{GUI_NAME:"Unused"},
                             },
                         2:{ TYPE:Raw_Data_Ref, GUI_NAME:"Device ID",
                             EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                             CHILD:{ TYPE:Bytearray_Raw, NAME:"Data",
                                     VISIBLE:False, SIZE:".Count"}
                             },
                         3:{ TYPE:Raw_Data_Ref, GUI_NAME:"Profile",
                             EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                             CHILD:{ TYPE:Bytearray_Raw, NAME:"Data",
                                     VISIBLE:False, SIZE:".Count"}
                             },
                         }
                     }
