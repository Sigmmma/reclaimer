#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.eqip import *
from .obje import *
from .item import *

eqip_attrs = desc_variant(eqip_attrs,
    ("grenade_type", SEnum16("grenade_type", *grenade_types_mcc)),
    )

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(3))
    )

eqip_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    eqip_attrs,

    SIZE=944,
    )

def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">", tag_cls=ObjeTag
    )
