#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.unit import *
from supyr_struct.util import desc_variant    

metagame_scoring = Struct("metagame_scoring",
    SEnum16("metagame_type", TOOLTIP="Used to determine score in MCC", *actor_types_mcc),
    SEnum16("metagame_class", TOOLTIP="Used to determine score in MCC", *actor_classes_mcc),
    Pad(8),
    )

unit_attrs = desc_variant(unit_attrs,
    ("mcc_additions", metagame_scoring),
    ("grenade_type", SEnum16("grenade_type", *grenade_types_mcc)),
    )

unit_body = Struct('tagdata',
    unit_attrs,
    SIZE=372
    )

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
