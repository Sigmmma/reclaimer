from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

efpp_attrs = Struct("efpp attrs",
    Pad(12),
    QStruct("quad tesselation",
        BSInt16("x"), BSInt16("y"),
        ORIENT='h'
        ),
    QStruct("x screen bounds", INCLUDE=from_to, MIN=0.0, MAX=1.0),
    QStruct("y screen bounds", INCLUDE=from_to, MIN=0.0, MAX=1.0),
    SIZE=60
    )


efpp_body = Struct("tagdata", efpp_attrs)

def get():
    return efpp_def

efpp_def = TagDef("efpp",
    blam_header_os('efpp'),
    efpp_body,

    ext=".effect_postprocess", endian=">"
    )
