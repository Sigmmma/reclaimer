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
    return srac_def

srac_def = TagDef("srac",
    blam_header('srac'),
    Struct('tagdata',
        ),

    ext=".shadowrun_actor", endian=">"
    )
