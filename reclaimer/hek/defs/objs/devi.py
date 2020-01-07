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

class DeviTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        devi_attrs = self.data.tagdata.devi_attrs

        devi_attrs.inv_power_acceleration_time = 0
        devi_attrs.inv_power_transition_time = 0
        devi_attrs.inv_position_acceleration_time = 0
        devi_attrs.inv_position_transition_time = 0
        devi_attrs.inv_depowered_acceleration_time = 0
        devi_attrs.inv_depowered_transition_time = 0

        if devi_attrs.power_acceleration_time:
            devi_attrs.inv_power_acceleration_time = 1 / (
                30 * devi_attrs.power_acceleration_time)

        if devi_attrs.power_transition_time:
            devi_attrs.inv_power_transition_time = 1 / (
                30 * devi_attrs.power_transition_time)

        if devi_attrs.depowered_position_acceleration_time:
            devi_attrs.inv_depowered_acceleration_time = 1 / (
                30 * devi_attrs.depowered_position_acceleration_time)

        if devi_attrs.depowered_position_transition_time:
            devi_attrs.inv_depowered_transition_time = 1 / (
                30 * devi_attrs.depowered_position_transition_time)

        if devi_attrs.position_acceleration_time:
            devi_attrs.inv_position_acceleration_time = 1 / (
                30 * devi_attrs.position_acceleration_time)

        if devi_attrs.position_transition_time:
            devi_attrs.inv_position_transition_time = 1 / (
                30 * devi_attrs.position_transition_time)
