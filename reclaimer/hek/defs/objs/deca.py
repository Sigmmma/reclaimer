#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag

class DecaTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        # why is this hardcoded, but exposed to the user?
        self.data.tagdata.maximum_sprite_extend = 16.0
