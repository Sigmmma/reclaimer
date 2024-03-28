#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.obje import *

obje_attrs = desc_variant(obje_attrs,
    dependency('animation_graph', valid_model_animations_yelo)
    )
obje_attrs = obje_attrs_variant(obje_attrs)

def get():
    return obje_def

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=ObjeTag
    )
