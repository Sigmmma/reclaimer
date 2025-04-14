#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.mod2 import *

def get():
    return mod2_def

permutation = desc_variant(permutation,
    reflexive("local_markers",
        local_marker, 64, DYN_NAME_PATH=".name", EXT_MAX=SINT16_MAX
        )
    )
region = desc_variant(region,
    reflexive("permutations",
        permutation, 32, DYN_NAME_PATH=".name", EXT_MAX=UINT8_MAX
        )
    )

mod2_body = desc_variant(mod2_body,
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    )
fast_mod2_body = desc_variant(fast_mod2_body,
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    )

mod2_def = TagDef("mod2",
    blam_header('mod2', 5),
    mod2_body,
    ext=".gbxmodel", endian=">", tag_cls=Mod2Tag
    )

fast_mod2_def = TagDef("mod2",
    blam_header('mod2', 5),
    mod2_body,
    ext=".gbxmodel", endian=">", tag_cls=Mod2Tag
    )
