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
    return t1ed_def

t1ed_def = TagDef("t1ed",
    blam_header('t1ed'),
    Struct('tagdata',
        ),

    ext=".tech_1_effect_data", endian=">"
    )
