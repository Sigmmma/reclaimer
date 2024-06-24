#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag

class Mgs2Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        for frame in self.data.tagdata.frames.STEPTREE:
            if frame.offset_exponent <= 0:
                frame.offset_exponent = 1.0

            if frame.radius_exponent <= 0:
                frame.radius_exponent = 1.0