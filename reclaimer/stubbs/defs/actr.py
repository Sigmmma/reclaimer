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

actr_body = dict(actr_body)
actr_body[3] = SEnum16("type", *actor_types)
actr_body[12] = dict(actr_body[12])
actr_body[12][2] = SEnum16("leader_type", *actor_types)

actr_body[14] = dict(actr_body[14])
actr_body[14][6] = SEnum16("defensive_crouch_type",
    "never",
    "danger",
    "low_shields",
    "hide_behind_shield",
    "any_target",
    )


def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header_stubbs('actr', 2),
    actr_body,

    ext=".actor", endian=">", tag_cls=ActrTag
    )
