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
from supyr_struct.util import desc_variant

panic = desc_variant(panic,
    ("leader_type", SEnum16("leader_type", *actor_types))
    )

defensive = desc_variant(defensive,
    ("defensive_crouch_type", SEnum16('defensive_crouch_type',
        "never",
        "danger",
        "low_shields",
        "hide_behind_shield",
        "any_target",
        )
     )
    )

actr_body = Struct("tagdata",
    flags,
    more_flags,

    Pad(12),
    SEnum16("type", *actor_types),  # NOTE: Stubbs actor types

    Pad(2),
    perception,

    Pad(8),
    movement,

    Pad(4),
    looking,

    unopposable,

    Pad(8),
    panic,

    Pad(28),
    defensive,

    Pad(4),
    pursuit,

    Pad(32),
    berserk,

    Pad(12),
    firing_positions,

    Pad(40),
    communication,
    SIZE=1272
    )


def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header_stubbs('actr', 2),
    actr_body,

    ext=".actor", endian=">", tag_cls=ActrTag
    )
