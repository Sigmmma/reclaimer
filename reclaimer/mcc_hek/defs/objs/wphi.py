#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag

class WphiTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        tagdata = self.data.tagdata
        tagdata.crosshair_types.data = 0

        for crosshair in tagdata.crosshairs.STEPTREE:
            tagdata.crosshair_types.data |= 1 << crosshair.crosshair_type.data
