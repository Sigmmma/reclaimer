from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

devc_body = Struct("tagdata",
    BSEnum16("device type",
        "mouse and keyboard",
        "joysticks/joypads/etc",
        "full profile definition",
        ),
    BBool16("flags",
        "unused",
        ),
    rawdata_ref("device id"),
    rawdata_ref("profile"),
    SIZE=44,
    )


def get():
    return devc_def

devc_def = TagDef(
    blam_header('devc'),
    devc_body,
    
    NAME="input_device_defaults",
    
    ext=".input_device_defaults", def_id="devc", endian=">"
    )
