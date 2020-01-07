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
    return m3ed_def

m3ed_def = TagDef("m3ed",
    blam_header('m3ed'),
    QStruct('tagdata',
        ),

    ext=".magic_3_effect_data", endian=">"
    )
