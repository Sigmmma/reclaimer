from .obje import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=6)

scen_body = Struct("tagdata",
    obje_attrs,
    SIZE=508,
    )


def get():
    return scen_def

scen_def = TagDef("scen",
    blam_header('scen'),
    scen_body,

    ext=".scenery", endian=">", tag_cls=HekTag
    )
