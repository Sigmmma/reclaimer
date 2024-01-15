#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.font import *
from supyr_struct.util import desc_variant

flags = Bool32("flags",
    "never_override_with_remastered_font_under_mcc",
    )
font_body = desc_variant(font_body,
    ("flags", flags)
    )

def get(): 
    return font_def

font_def = TagDef("font",
    blam_header('font'),
    font_body,

    ext=".font", endian=">", tag_cls=HekTag
    )
