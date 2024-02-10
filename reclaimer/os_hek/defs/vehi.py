#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.vehi import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "vehi")
vehi_body  = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    vehi_attrs,
    SIZE=1008,
    )

def get():
    return vehi_def

vehi_def = TagDef("vehi",
    blam_header('vehi'),
    vehi_body,

    ext=".vehicle", endian=">", tag_cls=ObjeTag
    )
