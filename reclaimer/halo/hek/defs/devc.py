from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

devc_body = Struct("Data",
    BSEnum16("device type",
        "mouse and keyboard",
        "joysticks/joypads/etc",
        "full profile definition",
        ),
    BBool16("Flags",
        "Unused",
        ),
    RawDataRef("device id",
        EDITABLE=False, INCLUDE=Raw_Data_Ref_Struct,
        CHILD=BytearrayRaw("data", VISIBLE=False, SIZE=".Count")
        ),
    RawDataRef("profile",
        EDITABLE=False, INCLUDE=Raw_Data_Ref_Struct,
        CHILD=BytearrayRaw("data", VISIBLE=False, SIZE=".Count")
        ),
    SIZE=44,
    )


def get():
    return devc_def

devc_def = TagDef(
    com( {1:{DEFAULT:"devc" }}, Tag_Header),
    devc_body,
    
    NAME="input_device_defaults",
    
    ext=".input_device_defaults", def_id="devc", endian=">"
    )
