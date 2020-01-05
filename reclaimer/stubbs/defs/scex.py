#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scex import *
from .schi import *
from supyr_struct.defs.tag_def import TagDef

scex_body = Struct("tagdata",
    shdr_attrs,
    scex_attrs,
    SIZE=120
    )

def get():
    return scex_def

scex_def = TagDef("scex",
    blam_header_stubbs('scex'),
    scex_body,

    ext=".shader_transparent_chicago_extended", endian=">", tag_cls=ShdrTag
    )
