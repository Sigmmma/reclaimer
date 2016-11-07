from .coll import *

sbsp_body = Struct("tagdata",
    SIZE=648,
    )


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    blam_header("sbsp", 5),
    sbsp_body,

    ext=".scenario_structure_bsp", endian=">",
    )
