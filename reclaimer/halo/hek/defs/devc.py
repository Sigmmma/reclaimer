from ...common_descs import *
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

devc_def = TagDef("devc",
    blam_header('devc'),
    devc_body,

    ext=".input_device_defaults", endian=">"
    )
