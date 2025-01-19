#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.soso import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

soso_attrs = desc_variant(soso_attrs,
    ("pad_11", Float("bump_scale")),
    ("pad_12", dependency_stubbs("bump_map", "bitm")),
    )

soso_body = Struct("tagdata",
    shdr_attrs,
    soso_attrs
    )

def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header_stubbs('soso', 3),
    soso_body,

    ext=".shader_model", endian=">",  # increment to differentiate it from halo soso
    tag_cls=ShdrTag
    )
