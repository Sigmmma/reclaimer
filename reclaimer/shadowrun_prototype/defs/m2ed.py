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
    return m2ed_def

m2ed_def = TagDef("m2ed",
    blam_header('m2ed'),
    QStruct('tagdata',
        ),

    ext=".magic_2_effect_data", endian=">"
    )
