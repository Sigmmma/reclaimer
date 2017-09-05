from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

devc_body = Struct("tagdata",
    SEnum16("device type",
        "mouse and keyboard",
        "joysticks/joypads/etc",
        "full profile definition",
        ),
    Bool16("flags",
        "unused",
        ),
    rawdata_ref("device id", max_size=16),
    rawdata_ref("profile", max_size=41984),
    SIZE=44,
    )

def get():
    return devc_def

devc_def = TagDef("devc",
    blam_header('devc'),
    devc_body,

    ext=".input_device_defaults", endian=">", tag_cls=HekTag
    )
