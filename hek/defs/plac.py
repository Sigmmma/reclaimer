from .obje import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=10)

plac_body = Struct("tagdata",
    obje_attrs,
    SIZE=508,
    )


def get():
    return plac_def

plac_def = TagDef("plac",
    blam_header('plac', 2),
    plac_body,

    ext=".placeholder", endian=">", tag_cls=HekTag
    )
