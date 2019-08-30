from reclaimer.hek.defs.objs.obje import ObjeTag
from reclaimer.hek.defs.objs.devi import DeviTag

class CtrlTag(DeviTag, ObjeTag):

    def calc_internal_data(self):
        ObjeTag.calc_internal_data(self)
        DeviTag.calc_internal_data(self)
