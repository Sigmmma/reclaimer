#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import sin, cos

from reclaimer.hek.defs.objs.tag import HekTag

class LighTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        shape = self.data.tagdata.shape
        shape.cosine_falloff_angle = cos(shape.falloff_angle)
        shape.cosine_cutoff_angle  = cos(shape.cutoff_angle)
        shape.sine_cutoff_angle    = sin(shape.cutoff_angle)
