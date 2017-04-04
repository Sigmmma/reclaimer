from ...hek.defs.obje import *

def get():
    return obje_def

obje_attrs = dict(obje_attrs)
obje_attrs[7] = dependency('model', 'mode')

obje_body = Struct('tagdata',
    obje_attrs,
    SIZE=380
    )

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">"
    )
