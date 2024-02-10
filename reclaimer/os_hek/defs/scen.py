#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scen import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "scen")
scen_body  = desc_variant(scen_body,  obje_attrs)

def get():
    return scen_def

scen_def = TagDef("scen",
    blam_header('scen'),
    scen_body,

    ext=".scenery", endian=">", tag_cls=ObjeTag
    )
