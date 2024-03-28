#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.actv import *

grenades  = desc_variant(actv_grenades, SEnum16("grenade_type", *grenade_types_os))
actv_body = desc_variant(actv_body, grenades)

def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
