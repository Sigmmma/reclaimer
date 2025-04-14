#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.weap import *
from .obje import *
from .item import *

magazine = desc_variant(magazine,
    reflexive("magazine_items", magazine_item, 8,
        "primary",
        "secondary_primary_2",
        # so uh, spv3 does a thing with extra ammo pickups that
        # act as alternate ammo counts for the primary magazine
        *("primary_%s" % (3 + i) for i in range(6))
        ),
    )
weap_attrs = desc_variant(weap_attrs,
    reflexive("magazines", magazine, 2, "primary", "secondary")
    )

obje_attrs = obje_attrs_variant(obje_attrs, "weap")
weap_body  = desc_variant(weap_body, obje_attrs, weap_attrs)

def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">", tag_cls=WeapTag
    )
