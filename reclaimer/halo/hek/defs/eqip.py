from .obje import *
from .item import *
from supyr_struct.defs.tag_def import TagDef

eqip_body = Struct("tagdata",
    object_attrs,
    item_attrs,
    BSEnum16('powerup type',
        'none',
        'double speed',
        'overshield',
        'active camo',
        'full-spectrum vision',
        'health',
        'grenade',
        ),
    BSEnum16('grenade type',
        'human frag',
        'covenant plasma',
        ),
    BFloat('powerup time'),
    dependency('pickup sound', valid_sounds),

    SIZE=944,
    )


def get():
    return eqip_def

eqip_def = TagDef("eqip",
    blam_header('eqip', 2),
    eqip_body,

    ext=".equipment", endian=">"
    )
