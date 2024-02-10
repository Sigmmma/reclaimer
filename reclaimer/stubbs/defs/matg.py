#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.matg import *
from supyr_struct.defs.tag_def import TagDef
from ..common_descs import *

def get():
    return matg_def

matg_body = desc_variant(matg_body,
    reflexive("grenades", grenade, len(grenade_types), *grenade_types),
    reflexive("materials", material, len(materials_list), *materials_list),
    )

matg_def = TagDef("matg",
    blam_header_stubbs('matg', 3),
    matg_body,

    ext=".globals", endian=">"
    )
