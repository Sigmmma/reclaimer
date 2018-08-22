from .tag import *

class PphyTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        tagdata = self.data.tagdata

        d = tagdata.density
        tagdata.scaled_density = d * 355840 / 3

        try:
            tagdata.water_gravity_scale = -((d - 1) / (d + 1))
        except ZeroDivisionError:
            tagdata.water_gravity_scale = float("-inf")

        # 0.0011 is the density of air relative to water
        try:
            tagdata.air_gravity_scale = -((d / 0.0011 - 1) /
                                          (d / 0.0011 + 1))
        except ZeroDivisionError:
            tagdata.air_gravity_scale = float("-inf")
