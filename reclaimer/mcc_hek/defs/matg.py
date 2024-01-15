#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.matg import *
from supyr_struct.util import desc_variant

matg_body = desc_variant(matg_body,
    ("grenades", reflexive("grenades", grenade, 4, *grenade_types_mcc)),
    )

def get():
    return matg_def

matg_def = TagDef("matg",
    blam_header('matg', 3),
    matg_body,

    ext=".globals", endian=">", tag_cls=HekTag
    )
