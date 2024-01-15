#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.ssce import *
from .obje import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(11))
    )

ssce_body = Struct("tagdata",
    obje_attrs,
    SIZE=508,
    )

def get():
    return ssce_def

ssce_def = TagDef("ssce",
    blam_header('ssce'),
    ssce_body,

    ext=".sound_scenery", endian=">", tag_cls=ObjeTag
    )
