#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return t3ed_def

t3ed_def = TagDef("t3ed",
    blam_header('t3ed'),
    Struct('tagdata',
        ),

    ext=".tech_3_effect_data", endian=">"
    )
