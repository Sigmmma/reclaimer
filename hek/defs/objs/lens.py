from math import cos

from reclaimer.hek.defs.objs.tag import HekTag

class LensTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        
        tagdata = self.data.tagdata
        tagdata.cosine_falloff_angle = cos(tagdata.falloff_angle)
        tagdata.cosine_cutoff_angle  = cos(tagdata.cutoff_angle)
