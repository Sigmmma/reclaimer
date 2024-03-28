#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.eqip import *
from .item import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "eqip")
eqip_attrs = desc_variant(eqip_attrs, SEnum16('grenade_type', *grenade_types))

eqip_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    eqip_attrs,
    SIZE=944,
    )

def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header_stubbs('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">", tag_cls=ObjeTag
    )
