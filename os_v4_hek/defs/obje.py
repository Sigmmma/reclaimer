from ...os_v3_hek.defs.obje import *

obje_attrs = dict(obje_attrs)
obje_attrs[1] = Bool16('flags',
    'does not cast shadow',
    'transparent self-occlusion',
    'brighter than it should be',
    'not a pathfinding obstacle',
    'cast shadow by default',
    ('xbox_unknown_bit_8', 1<<8),
    ('xbox_unknown_bit_11', 1<<11),
    )

obje_body = Struct('tagdata',
    obje_attrs
    )

def get():
    return obje_def

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=HekTag
    )
