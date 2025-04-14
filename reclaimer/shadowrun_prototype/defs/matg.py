#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.matg import *

def get():
    return matg_def

# shadowrun has more grenade types
matg_body = desc_variant(matg_body,
    reflexive("grenades", grenade, 5)
    )

matg_def = TagDef("matg",
    blam_header_os('matg', 3),
    matg_body,

    ext=".globals", endian=">", tag_cls=HekTag
    )
