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

obje_attrs = obje_attrs_variant(obje_attrs, "garb")
garb_body  = desc_variant(garb_body, obje_attrs)

def get():
    return garb_def

garb_def = TagDef("grab",
    blam_header_stubbs('garb'),
    garb_body,

    ext=".garbage", endian=">", tag_cls=ObjeTag
    )
