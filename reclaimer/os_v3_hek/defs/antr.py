#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_hek.defs.antr import *

antr_body = desc_variant(antr_body,
    # open sauce increases all these
    # https://github.com/HaloMods/OpenSauce/blob/master/OpenSauce/shared/Include/blamlib/Halo1/models/model_animation_definitions.hpp
    reflexive("units", unit_desc, 64, DYN_NAME_PATH=".label"),
    reflexive("sound_references", sound_reference_desc, 257*2,
        DYN_NAME_PATH=".sound.filepath"
        ),
    reflexive("animations", animation_desc, 2048, DYN_NAME_PATH=".name")
    )

def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )