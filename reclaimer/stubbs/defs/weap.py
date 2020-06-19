#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.weap import *
from .obje import *
from .item import *
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(2))
    )

weap_attrs = desc_variant(weap_attrs,
    ("weapon_type", SEnum16('weapon_type', *weapon_types))
    )

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
