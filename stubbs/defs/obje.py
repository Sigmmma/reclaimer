from ...hek.defs.obje import *
from ..common_descs import *

def get():
    return obje_def

obje_attrs = dict(obje_attrs)
obje_attrs[7] = dependency_stubbs('model', 'mode')

obje_body = Struct('tagdata',
    obje_attrs,
    SIZE=380
    )

obje_def = TagDef("obje",
    blam_header_stubbs('obje'),
    obje_body,

    ext=".object", endian=">"
    )

def get():
    return obje_def
