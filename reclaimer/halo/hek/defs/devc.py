from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return DevcDef

class DevcDef(TagDef):

    ext = ".input_device_defaults"

    tag_id = "devc"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"input_device_defaults",
                     0:com( {1:{ DEFAULT:"devc" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:44, GUI_NAME:"Data",
                         0:{ TYPE:Enum16, GUI_NAME:"Device Type",
                             0:{ GUI_NAME:"Mouse and keyboard" },
                             1:{ GUI_NAME:"Joysticks/joypads/etc" },
                             2:{ GUI_NAME:"Full profile definition" },
                             },
                         1:{ TYPE:Bool16, GUI_NAME:"Flags",
                             0:{GUI_NAME:"Unused"},
                             },
                         2:{ TYPE:RawDataRef, GUI_NAME:"Device ID",
                             EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                             CHILD:{ TYPE:BytearrayRaw, NAME:"Data",
                                     VISIBLE:False, SIZE:".Count"}
                             },
                         3:{ TYPE:RawDataRef, GUI_NAME:"Profile",
                             EDITABLE:False, INCLUDE:Raw_Data_Ref_Struct,
                             CHILD:{ TYPE:BytearrayRaw, NAME:"Data",
                                     VISIBLE:False, SIZE:".Count"}
                             }
                         }
                     }
