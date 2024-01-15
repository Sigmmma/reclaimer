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

obje_flags = Bool16('flags',
    'does_not_cast_shadow',
    'transparent_self_occlusion',
    'brighter_than_it_should_be',
    'not_a_pathfinding_obstacle',
    "extension_of_parent",
    "cast_shadow_by_default",
    "does_not_have_remastered_geometry",
    {NAME: 'xbox_unknown_bit_8', VALUE: 1<<8, VISIBLE: False},
    {NAME: 'xbox_unknown_bit_11', VALUE: 1<<11, VISIBLE: False},
    )
obje_attrs = desc_variant(obje_attrs,
    ("flags", obje_flags),
    )

obje_body = Struct('tagdata',
    obje_attrs,
    SIZE=380
    )

def get():
    return obje_def

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=ObjeTag
    )
