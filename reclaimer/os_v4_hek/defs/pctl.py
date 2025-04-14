#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.pctl import *

shader_extensions = reflexive("shader_extensions",
    Struct("shader_extension", INCLUDE=os_shader_extension), 1
    )
particle_state = desc_variant(particle_state,
    ("pad_19", shader_extensions),
    )
particle_type  = desc_variant(particle_type,
    reflexive("particle_states", particle_state, 8, DYN_NAME_PATH='.name'),
    )
pctl_body      = desc_variant(pctl_body,
    reflexive("particle_types", particle_type, 4, DYN_NAME_PATH='.name'),
    )

def get():
    return pctl_def

pctl_def = TagDef("pctl",
    blam_header("pctl", 4),
    pctl_body,

    ext=".particle_system", endian=">", tag_cls=HekTag,
    )
