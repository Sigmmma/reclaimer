from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


control_point = Struct("control point",
    QStruct("position", INCLUDE=ijk_float),
    QStruct("orientation", INCLUDE=ijkw_float),
    SIZE=28,
    )

trak_body = Struct("tagdata",
    Pad(4),
    h2_reflexive("control points", control_point, 16),
    ENDIAN="<", SIZE=12
    )


def get():
    return trak_def

trak_def = TagDef("trak",
    h2_blam_header('trak'),
    trak_body,

    ext=".%s" % h2_tag_class_fcc_to_ext["trak"], endian="<"
    )
