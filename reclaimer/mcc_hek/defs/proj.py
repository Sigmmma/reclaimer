#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.proj import *
from .obje import *
from supyr_struct.util import desc_variant

potential_response_flags = Bool16("flags",
    "only_against_units",
    "never_against_units"
    )
potential_response_descs = [
    desc for desc in material_response.values()
    if isinstance(desc, dict) and desc.get("NAME") == "potential_response"
    ]
if not potential_response_descs:
    raise ValueError("Could not locate descriptor 'potential_response' in material_response")

potential_response = desc_variant(potential_response_descs[0],
    ("flags", potential_response_flags)
    )
material_response = desc_variant(material_response,
    ("potential_response", potential_response)
    )
material_responses = reflexive("material_responses",
    material_response, len(materials_list), *materials_list
    )

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(5))
    )
proj_attrs = desc_variant(proj_attrs,
    ("material_responses", material_responses)
    )

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

    ext=".projectile", endian=">", tag_cls=ObjeTag
    )
