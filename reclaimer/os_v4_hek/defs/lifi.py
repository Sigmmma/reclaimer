#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.lifi import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "lifi")
lifi_body  = desc_variant(lifi_body, obje_attrs)

def get():
    return lifi_def

lifi_def = TagDef("lifi",
    blam_header('lifi'),
    lifi_body,

    ext=".device_light_fixture", endian=">", tag_cls=LifiTag
    )
