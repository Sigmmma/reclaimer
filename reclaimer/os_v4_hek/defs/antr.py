#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.antr import *

unit_desc = desc_variant(unit_desc,
    reflexive("animations", anim_enum_desc,
        len(unit_animation_names_os),
        *unit_animation_names_os
        )
    )

antr_body = desc_variant(antr_body,
    # this was further increased in os v4
    # https://github.com/HaloMods/OpenSauce/blob/master/OpenSauce/shared/Include/blamlib/Halo1/models/model_animation_definitions.hpp#L21
    reflexive("units", unit_desc, 512, DYN_NAME_PATH=".label"),
    )

def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )