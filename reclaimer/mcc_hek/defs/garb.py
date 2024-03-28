#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.garb import *
from .obje import *
from .item import *

obje_attrs = obje_attrs_variant(obje_attrs, "garb")
garb_body = Struct("tagdata",
    obje_attrs,
    item_attrs,

    SIZE=944,
    )

def get():
    return garb_def

garb_def = TagDef("garb",
    blam_header('garb'),
    garb_body,

    ext=".garbage", endian=">", tag_cls=ObjeTag
    )
