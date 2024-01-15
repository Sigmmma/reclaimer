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

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(6))
    )

scen_body = Struct("tagdata",
    obje_attrs,

    SIZE=508,
    )

def get():
    return scen_def

scen_def = TagDef("scen",
    blam_header('scen'),
    scen_body,

    ext=".scenery", endian=">", tag_cls=ObjeTag
    )
