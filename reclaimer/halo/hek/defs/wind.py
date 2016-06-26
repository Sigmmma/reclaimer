from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

wind_body = Struct("tagdata",
    #I didnt feel like adding offsets since there is no
    #padding until AFTER all entries. it's all sequential
    Struct("velocity",       INCLUDE=from_to),
    Struct("variation area", INCLUDE=yp_float),
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
