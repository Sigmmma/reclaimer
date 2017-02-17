from .pc_gametype import *

class XboxGametypeTag(PcGametypeTag):
    def __init__(self, *args, **kwargs):
        PcGametypeTag.__init__(self, *args, **kwargs)
        self.is_xbox = True
