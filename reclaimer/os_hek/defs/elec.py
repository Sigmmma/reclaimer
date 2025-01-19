#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.elec import *

def get():
    return elec_def

shader = desc_variant(shader,
    ("secondary_map", Pad(104)),
    verify=False
    )
elec_body = desc_variant(elec_body,
    reflexive("shaders", shader, 1),
    )

elec_def = TagDef("elec",
    blam_header("elec"),
    elec_body,

    ext=".lightning", endian=">", tag_cls=HekTag,
    )
