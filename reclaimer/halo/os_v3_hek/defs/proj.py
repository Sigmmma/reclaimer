from ...hek.defs.proj import *

#import and use the open saucified obje attrs
from .obje import *

proj_body = dict(proj_body)
proj_body[0] = obje_attrs

def get():
    return proj_def

proj_def = TagDef("proj",
    blam_header('proj', 5),
    proj_body,

    ext=".projectile", endian=">"
    )