#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.util.matrices import euler_2d_to_vector_3d

class EffeTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        for event in self.data.tagdata.events.STEPTREE:
            for particle in event.particles.STEPTREE:
                particle.relative_direction_vector[:] = euler_2d_to_vector_3d(
                    *particle.relative_direction
                    )
