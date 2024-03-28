#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.bipd import *
from .obje import *
from .unit import *

obje_attrs = obje_attrs_variant(obje_attrs, "bipd")
bipd_body  = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    bipd_attrs,
    SIZE=1268,
    )

def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">", tag_cls=BipdTag
    )
