#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_hek.defs.weap import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "weap")
weap_body  = desc_variant(weap_body, obje_attrs)

def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">", tag_cls=WeapTag
    )
