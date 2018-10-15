from .tag import *

class WphiTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        tagdata = self.data.tagdata
        tagdata.crosshair_types.data = 0

        for crosshair in tagdata.crosshairs.STEPTREE:
            tagdata.crosshair_types.data |= 1 << crosshair.crosshair_type.data
