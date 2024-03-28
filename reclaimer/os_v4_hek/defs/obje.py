#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.obje import *

obje_attrs = desc_variant(obje_attrs,
    Bool16('flags',
        'does_not_cast_shadow',
        'transparent_self_occlusion',
        'brighter_than_it_should_be',
        'not_a_pathfinding_obstacle',
        'cast_shadow_by_default',
        ),
    )

obje_body = Struct('tagdata',
    obje_attrs
    )

def get():
    return obje_def

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=ObjeTag
    )
