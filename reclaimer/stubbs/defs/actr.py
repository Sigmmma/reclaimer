#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.actr import *
from ..common_descs import *

panic     = desc_variant(panic, SEnum16("leader_type", *actor_types))
actr_body = desc_variant(actr_body, SEnum16("type", *actor_types), panic)

def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header_stubbs('actr', 2),
    actr_body,

    ext=".actor", endian=">", tag_cls=ActrTag
    )
