#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.obje import ObjeTag
from reclaimer.hek.defs.objs.devi import DeviTag

class MachTag(DeviTag, ObjeTag):

    def calc_internal_data(self):
        ObjeTag.calc_internal_data(self)
        DeviTag.calc_internal_data(self)
        mach_attrs = self.data.tagdata.mach_attrs
        mach_attrs.door_open_time_ticks = int(mach_attrs.door_open_time * 30)
