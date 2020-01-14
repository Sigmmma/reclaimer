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
#from reclaimer.common_descs import valid_objects

class EffeTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        never_cull = False
        for event in self.data.tagdata.events.STEPTREE:
            for part in event.parts.STEPTREE:
                if part.type.tag_class.enum_name == 'light':
                    never_cull = True

                part.effect_class = part.type.tag_class

                #TODO: There is no good way to do this right now
                #object_types = valid_objects('b').desc[0]['NAME_MAP'].keys()
                #if part.effect_class.enum_name in object_types:
                #    part.effect_class.enum_name = 'object'

            for particle in event.particles.STEPTREE:
                particle.relative_direction_vector[:] = euler_2d_to_vector_3d(
                    *particle.relative_direction
                    )
        self.data.tagdata.flags.never_cull = never_cull
