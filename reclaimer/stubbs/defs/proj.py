#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.proj import *
from ..common_descs import *
from .obje import *

obje_attrs = obje_attrs_variant(obje_attrs, "proj")

material_responses = reflexive("material_responses", 
    material_response, len(materials_list), *materials_list
    )
proj_attrs = desc_variant(proj_attrs,  material_responses)

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

    ext=".projectile", endian=">", tag_cls=ObjeTag
    )
