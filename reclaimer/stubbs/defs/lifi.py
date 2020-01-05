#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .devi import *
from ...hek.defs.lifi import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=9)

lifi_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,

    SIZE=720,
    )

def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header_stubbs('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">", tag_cls=LifiTag
    )
