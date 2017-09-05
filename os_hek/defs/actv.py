from ...hek.defs.actv import *

# grenades descriptor index in actv_body is 10
# grenade_type descriptor index in grenades_desc is 1

# replace the grenade_type descriptor with one
# that uses open sauce's extra grenade slots
actv_body = dict(actv_body)
grenades_desc = actv_body[10] = dict(actv_body[10])
grenades_desc[1] = SEnum16("grenade type", *grenade_types_os)

def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
