#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.spla import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

spla_body = Struct("tagdata",
    shdr_attrs,
    spla_attrs,
    SIZE=332,
    )


def get():
    return spla_def

spla_def = TagDef("spla",
    blam_header_stubbs('spla'),
    spla_body,

    ext=".shader_transparent_plasma", endian=">", tag_cls=ShdrTag
    )
