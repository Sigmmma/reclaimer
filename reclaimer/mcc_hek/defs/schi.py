#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.schi import *
from .shdr import *

extra_flags = Bool32("extra_flags",
    "dont_fade_active_camouflage",
    "numeric_countdown_timer",
    "custom_edition_blending",
    )
schi_attrs = desc_variant(schi_attrs, extra_flags)

schi_body = Struct("tagdata",
    shdr_attrs,
    schi_attrs,
    SIZE=108
    )

def get():
    return schi_def

schi_def = TagDef("schi",
    blam_header('schi'),
    schi_body,

    ext=".shader_transparent_chicago",
    endian=">", tag_cls=ShdrTag
    )
