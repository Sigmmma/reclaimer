#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.jpt_ import *
from .cdmg import damage_flags

damage = desc_variant(damage,
    damage_flags,
    QStruct("instantaneous_acceleration", INCLUDE=ijk_float, SIDETIP="[-inf,+inf]"),
    ("pad_13", Pad(0)),
    # we're doing some weird stuff to make this work, so we're turning off verify
    verify=False
    )

jpt__body = desc_variant(jpt__body, damage)

def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    blam_header('jpt!', 6),
    jpt__body,

    ext=".damage_effect", endian=">", tag_cls=HekTag,
    )
