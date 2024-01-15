#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.mach import *
from .obje import *
from .devi import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(7))
    )

mach_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    mach_attrs,

    SIZE=804,
    )

def get():
    return mach_def

mach_def = TagDef("mach",
    blam_header('mach'),
    mach_body,

    ext=".device_machine", endian=">", tag_cls=MachTag
    )
