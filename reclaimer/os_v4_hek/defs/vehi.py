#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.vehi import *
from .obje import *
from .unit import *

obje_attrs = obje_attrs_variant(obje_attrs, "vehi")
vehi_body  = desc_variant(vehi_body, obje_attrs, unit_attrs)

def get():
    return vehi_def

vehi_def = TagDef("vehi",
    blam_header('vehi'),
    vehi_body,

    ext=".vehicle", endian=">", tag_cls=ObjeTag
    )
