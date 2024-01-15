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

metagame_scoring = Struct("metagame_scoring",
    SEnum16("metagame_type", *actor_types_mcc),
    SEnum16("metagame_class", *actor_classes_mcc),
    ORIENT="H", COMMENT="Used to determine score in MCC", 
    )

actv_grenades = desc_variant(actv_grenades,
    ("grenade_type", SEnum16("grenade_type", *grenade_types_mcc)),
    )
actv_body = desc_variant(actv_body,
    ("grenades", actv_grenades),
    ("pad_4", metagame_scoring),
    )

def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
