#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.hudg import *
from supyr_struct.util import desc_variant

targets = Struct("targets",
    dependency("target_bitmap", "bitm"),
    SEnum16("language",
        "english",
        "french",
        "spanish",
        "italian",
        "german",
        "tchinese",
        "japanese",
        "korean",
        "portuguese",
        "latam_spanish",
        "polish",
        "russian",
        "schinese"
        ),
    Bool16("flags",
        "legacy_mode"
        ),
    SIZE=20
    )

remap = Struct("remap",
    dependency("original_bitmap", "bitm"),
    reflexive("targets", targets, 26, DYN_NAME_PATH='.target_bitmap.filepath'),
    SIZE=28
    )
remaps = reflexive("remaps", remap, 32, DYN_NAME_PATH='.original_bitmap.filepath')

misc_hud_crap = desc_variant(misc_hud_crap,
    ("unknown", remaps)
    )
hudg_body = desc_variant(hudg_body,
    ("misc_hud_crap", misc_hud_crap)
    )

def get():
    return hudg_def

hudg_def = TagDef("hudg",
    blam_header("hudg"),
    hudg_body,

    ext=".hud_globals", endian=">", tag_cls=HekTag,
    )
