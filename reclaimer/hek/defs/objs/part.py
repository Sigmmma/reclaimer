#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag

class PartTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

         # crash if this is nonzero?
        self.data.tagdata.rendering.contact_deterioration = 0.0