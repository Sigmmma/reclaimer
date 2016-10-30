from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

wind_body = Struct("tagdata",
    QStruct("velocity",       INCLUDE=from_to),
    QStruct("variation area", INCLUDE=yp_float),
    BFloat("local variation weight"),
    BFloat("local variation rate"),
    BFloat("damping"),
    SIZE=64,
    )


def get():
    return wind_def

wind_def = TagDef("wind",
    blam_header('wind'),
    wind_body,

    ext=".wind", endian=">"
    )
