#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .item import *
from .objs.obje import ObjeTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=3)

eqip_attrs = Struct("eqip_attrs",
    SEnum16('powerup_type',
        'none',
        'double_speed',
        'overshield',
        'active_camo',
        'full_spectrum_vision',
        'health',
        'grenade',
        ),
    SEnum16('grenade_type', *grenade_types),
    float_sec('powerup_time'),
    dependency('pickup_sound', "snd!"),

    SIZE=168
    )

eqip_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    eqip_attrs,

    SIZE=944,
    )


def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">", tag_cls=ObjeTag
    )
