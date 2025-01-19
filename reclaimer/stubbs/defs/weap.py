#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.weap import *
from .item import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "weap")
weap_attrs = desc_variant(weap_attrs, SEnum16('weapon_type', *weapon_types))

weap_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    weap_attrs,
    SIZE=1288,
    )

def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header_stubbs('weap', 2),
    weap_body,

    ext=".weapon", endian=">", tag_cls=WeapTag
    )
