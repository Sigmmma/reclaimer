#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.cdmg import *
from ..common_descs import *

damage    = desc_variant(damage, SEnum16("category", *damage_category))
cdmg_body = desc_variant(cdmg_body, damage, damage_modifiers)

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header_stubbs('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">"
    )
