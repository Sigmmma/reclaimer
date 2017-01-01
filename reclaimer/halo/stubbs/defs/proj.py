from ...hek.defs.proj import *
from .obje import *
from ..common_descs import *
from .objs.tag import StubbsTag
from supyr_struct.defs.tag_def import TagDef

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
    blam_header('proj', 5),
    proj_body,

    ext=".projectile", endian=">"
    )
