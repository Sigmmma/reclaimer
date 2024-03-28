#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.jpt_ import *
from ..common_descs import *

damage    = desc_variant(damage, SEnum16("category", *damage_category))
jpt__body = desc_variant(jpt__body, damage, damage_modifiers)


def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header_stubbs('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">"
    )
