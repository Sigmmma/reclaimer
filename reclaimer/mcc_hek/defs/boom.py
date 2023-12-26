#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get():
    return boom_def

boom_def = TagDef("boom",
    blam_header('boom'),
    QStruct('tagdata',
        #this is just a guess. This could just as easily
        #be 4 bytes of padding. effing useless tag type
        Float('radius')
        ),

    ext=".spheroid", endian=">", tag_cls=HekTag
    )
