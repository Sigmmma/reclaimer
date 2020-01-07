#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.obje import ObjeTag

class WeapTag(ObjeTag):

    def calc_internal_data(self):
        ObjeTag.calc_internal_data(self)
        for trigger in self.data.tagdata.weap_attrs.triggers.STEPTREE:
            firing = trigger.firing
            misc = trigger.misc
            rates = trigger.misc_rates
            for i in range(len(rates)):
                rates[i] = 0

            if misc.ejection_port_recovery_time:
                rates.ejection_port_recovery_rate = 1 / misc.ejection_port_recovery_time
            if misc.illumination_recovery_time:
                rates.illumination_recovery_rate = 1 / misc.illumination_recovery_time

            if firing.acceleration_time:
                rates.acceleration_rate = 1 / firing.acceleration_time
            if firing.deceleration_time:
                rates.deceleration_rate = 1 / firing.deceleration_time

            if firing.error_acceleration_time:
                rates.error_acceleration_rate = 1 / firing.error_acceleration_time
            if firing.error_deceleration_time:
                rates.error_deceleration_rate = 1 / firing.error_deceleration_time

            for i in range(len(rates)):
                rates[i] /= 30
