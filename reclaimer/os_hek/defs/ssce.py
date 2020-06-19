#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.ssce import *

#import and use the open saucified obje attrs
from .obje import *
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(
    obje_attrs, (
        "object_type", FlSEnum16(
            "object_type",
            *((object_types[i], i - 1) for i in
              range(len(object_types))),
            VISIBLE=False, DEFAULT=11
            )
        )
    )

ssce_body = desc_variant(ssce_body,
    ("obje_attrs", obje_attrs),
    )

def get():
    return ssce_def

ssce_def = TagDef("ssce",
    blam_header('ssce'),
    ssce_body,

    ext=".sound_scenery", endian=">", tag_cls=ObjeTag
    )
