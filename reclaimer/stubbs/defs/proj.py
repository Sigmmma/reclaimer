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
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(5))
    )

proj_attrs = desc_variant(proj_attrs,
    ("material_responses", reflexive("material_responses",
        material_response, len(materials_list), *materials_list
        )
     )
    )

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
