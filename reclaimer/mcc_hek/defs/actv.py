#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.actv import *
from supyr_struct.util import desc_variant

actv_grenades = desc_variant(actv_grenades,
    ("grenade_type", SEnum16("grenade_type", *grenade_types_mcc)),
    )
metagame_scoring = Struct("metagame_scoring",
    SEnum16("metagame_type", *actor_types_mcc),
    SEnum16("metagame_class", *actor_classes_mcc),
    ORIENT="H", COMMENT="Used to determine score in MCC", 
    )
movement_switching_descs = [
    desc for desc in actv_body.values()
    if isinstance(desc, dict) and desc.get("NAME") == "movement_switching"
    ]
if not movement_switching_descs:
    raise ValueError("Could not locate descriptor 'movement_switching' in actv_body")
movement_switching = desc_variant(movement_switching_descs[0],
    ("pad_0", Pad(20)),
    )

actv_body = desc_variant(actv_body,
    ("grenades", actv_grenades),
    ("mcc_scoring_type", metagame_scoring),
    ("movement_switching", movement_switching),
    )

def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
