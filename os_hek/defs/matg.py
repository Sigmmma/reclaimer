from ...hek.defs.matg import *

def get():
    return matg_def

# replace the grenades reflexive with an open sauce one
matg_body = dict(matg_body)
matg_body[5] = reflexive("grenades", grenade, 4, *grenade_types_os)

matg_def = TagDef("matg",
    blam_header_os('matg', 3),
    matg_body,

    ext=".globals", endian=">", tag_cls=HekTag
    )
