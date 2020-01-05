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
from supyr_struct.defs.tag_def import TagDef

schi_body = Struct("tagdata",
    shdr_attrs,
    schi_attrs,
    SIZE=108
    )

def get():
    return schi_def

schi_def = TagDef("schi",
    blam_header_stubbs('schi'),
    schi_body,

    ext=".shader_transparent_chicago", endian=">", tag_cls=ShdrTag,
    )
