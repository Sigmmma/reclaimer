#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import cos

from reclaimer.hek.defs.objs.tag import HekTag

class ActrTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        perception = self.data.tagdata.perception
        looking = self.data.tagdata.looking

        perception.inv_combat_perception_time = 0
        perception.inv_guard_perception_time = 0
        perception.inv_non_combat_perception_time = 0

        if perception.combat_perception_time:
            perception.inv_combat_perception_time = 1 / perception.combat_perception_time

        if perception.guard_perception_time:
            perception.inv_guard_perception_time = 1 / perception.guard_perception_time

        if perception.non_combat_perception_time:
            perception.inv_non_combat_perception_time = 1 / perception.non_combat_perception_time

        perception.inv_combat_perception_time /= 30
        perception.inv_guard_perception_time /= 30
        perception.inv_non_combat_perception_time /= 30

        for i in range(2):
            looking.cosine_maximum_aiming_deviation[i]  = cos(looking.maximum_aiming_deviation[i])
            looking.cosine_maximum_looking_deviation[i] = cos(looking.maximum_looking_deviation[i])
