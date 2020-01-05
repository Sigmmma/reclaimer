#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.senv import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

senv_body = Struct("tagdata",
    shdr_attrs,
    senv_attrs,
    SIZE=836,
    )

def get():
    return senv_def

senv_def = TagDef("senv",
    blam_header_stubbs('senv', 2),
    senv_body,

    ext=".shader_environment", endian=">", tag_cls=ShdrTag
    )
