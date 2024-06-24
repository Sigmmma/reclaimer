#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.bipd import *
from .obje import *
from .unit import *

obje_attrs = obje_attrs_variant(obje_attrs, "bipd")
bipd_body  = desc_variant(bipd_body, obje_attrs, unit_attrs)

def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">", tag_cls=BipdTag
    )
