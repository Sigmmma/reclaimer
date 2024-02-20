#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.antr import *

antr_body = desc_variant(antr_body,
    # original maximum according to comment?
    # https://github.com/HaloMods/OpenSauce/blob/master/OpenSauce/Halo1/Halo1_CheApe/Halo1_CheApe_Readme.txt#L40
    reflexive("animations", animation_desc, 500, DYN_NAME_PATH=".name")
    )

def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
