from reclaimer.misc.defs.objs.pc_gametype import PcGametypeTag

class XboxGametypeTag(PcGametypeTag):
    def __init__(self, *args, **kwargs):
        PcGametypeTag.__init__(self, *args, **kwargs)
        self.is_xbox = True
