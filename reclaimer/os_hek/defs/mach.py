#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.mach import *

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
            VISIBLE=False, DEFAULT=7
            )
        )
    )

mach_body = desc_variant(mach_body,
    ("obje_attrs", obje_attrs),
    )

def get():
    return mach_def

mach_def = TagDef("mach",
    blam_header('mach'),
    mach_body,

    ext=".device_machine", endian=">", tag_cls=MachTag
    )
