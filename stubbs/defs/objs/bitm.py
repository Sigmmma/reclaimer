from reclaimer.hek.defs.objs.bitm import BitmTag
from reclaimer.bitmaps.p8_palette import STUBBS_P8_PALETTE

class StubbsBitmTag(BitmTag):
    def __init__(self, *args, **kwargs):
        BitmTag.__init__(self, *args, **kwargs)
        self.p8_palette = STUBBS_P8_PALETTE
