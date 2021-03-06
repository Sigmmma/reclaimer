#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .objs.obje import ObjeTag
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(10))
    )

plac_body = Struct("tagdata",
    obje_attrs,
    SIZE=508,
    )


def get():
    return plac_def

plac_def = TagDef("plac",
    blam_header('plac', 2),
    plac_body,

    ext=".placeholder", endian=">", tag_cls=ObjeTag
    )
