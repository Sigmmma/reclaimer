#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.proj import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "proj")
proj_body  = desc_variant(proj_body,  obje_attrs)

def get():
    return proj_def

proj_def = TagDef("proj",
    blam_header('proj', 5),
    proj_body,

    ext=".projectile", endian=">", tag_cls=ObjeTag
    )
