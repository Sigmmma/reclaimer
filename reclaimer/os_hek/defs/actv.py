#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from supyr_struct.util import desc_variant

from ...hek.defs.actv import *

# Create opensauce variant of grenade descriptor.

os_actv_grenades = desc_variant(actv_grenades,
    ("grenade_type", SEnum16("grenade_type", *grenade_types_os)),
)

# Create os variant of actv descriptor using the new grenade descriptor.

actv_body = desc_variant(actv_body,
    ("grenades", os_actv_grenades),
)

def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
