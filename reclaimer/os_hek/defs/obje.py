#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.obje import *
from supyr_struct.util import desc_variant

def get():
    return obje_def

obje_attrs = desc_variant(obje_attrs,
    ("animation_graph", dependency('animation_graph', valid_model_animations_yelo))
    )

obje_body = Struct('tagdata',
    obje_attrs
    )

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=ObjeTag
    )
