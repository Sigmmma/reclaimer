from .obje import *
from .item import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=3)

eqip_attrs = Struct("equipment attrs",
    SEnum16('powerup type',
        'none',
        'double speed',
        'overshield',
        'active camo',
        'full-spectrum vision',
        'health',
        'grenade',
        ),
    SEnum16('grenade type', *grenade_types),
    float_sec('powerup time'),
    dependency('pickup sound', "snd!"),

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

    ext=".equipment", endian=">", tag_cls=HekTag
    )
