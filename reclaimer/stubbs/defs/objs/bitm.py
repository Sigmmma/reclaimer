#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.bitm import BitmTag
from reclaimer.bitmaps.p8_palette import STUBBS_P8_PALETTE

class StubbsBitmTag(BitmTag):
    def __init__(self, *args, **kwargs):
        BitmTag.__init__(self, *args, **kwargs)
        self.p8_palette = STUBBS_P8_PALETTE
