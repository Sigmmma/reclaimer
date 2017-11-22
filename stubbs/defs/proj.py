from ...hek.defs.proj import *
from ..common_descs import *
from .obje import *
from supyr_struct.defs.tag_def import TagDef

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=5)

proj_attrs = dict(proj_attrs)
proj_attrs[13] = reflexive("material responses", material_response,
                           len(materials_list), *materials_list)

proj_body = Struct("tagdata",
    obje_attrs,
    proj_attrs,
    SIZE=588,
    )

def get():
    return proj_def

proj_def = TagDef("proj",
    blam_header_stubbs('proj', 5),
    proj_body,

    ext=".projectile", endian=">"
    )
