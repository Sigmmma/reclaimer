from ...os_v3_hek.defs.proj import *

#import and use the open saucified obje attrs
from .obje import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=5)

proj_body = dict(proj_body)
proj_body[0] = obje_attrs

def get():
    return proj_def

proj_def = TagDef("proj",
    blam_header('proj', 5),
    proj_body,

    ext=".projectile", endian=">", tag_cls=HekTag
    )
