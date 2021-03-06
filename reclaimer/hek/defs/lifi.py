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
from .objs.lifi import LifiTag
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(9))
    )

lifi_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,

    SIZE=720,
    )


def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">", tag_cls=LifiTag
    )
