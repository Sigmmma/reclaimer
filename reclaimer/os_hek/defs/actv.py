#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.actv import *

# TODO use some supyr trickery to make this nicer.

# grenades descriptor index in actv_body is 10
# grenade_type descriptor index in grenades_desc is 1

# replace the grenade_type descriptor with one
# that uses open sauce's extra grenade slots
actv_body = dict(actv_body)
grenades_desc = actv_body[10] = dict(actv_body[10])
grenades_desc[1] = SEnum16("grenade_type", *grenade_types_os)

def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
