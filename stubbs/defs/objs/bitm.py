from ....field_types import *
from ....hek.defs.objs.bitm import *

class StubbsBitmTag(BitmTag):
    def __init__(self, *args, **kwargs):
        BitmTag.__init__(self, *args, **kwargs)
        self.p8_palette = STUBBS_P8_PALETTE
