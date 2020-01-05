#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import sin, cos

from reclaimer.hek.defs.objs.obje import ObjeTag

class BipdTag(ObjeTag):

    def calc_internal_data(self):
        ObjeTag.calc_internal_data(self)
        bipd_attrs = self.data.tagdata.bipd_attrs
        movement = bipd_attrs.movement
        physics = bipd_attrs.physics

        physics.cosine_stationary_turning_threshold = cos(bipd_attrs.stationary_turning_threshold)

        physics.cosine_maximum_slope_angle = cos(movement.maximum_slope_angle)
        physics.neg_sine_downhill_falloff_angle = -sin(movement.downhill_falloff_angle)
        physics.neg_sine_downhill_cutoff_angle  = -sin(movement.downhill_cutoff_angle)
        physics.sine_uphill_falloff_angle = sin(movement.uphill_falloff_angle)
        physics.sine_uphill_cutoff_angle  = sin(movement.uphill_cutoff_angle)

        physics.crouch_camera_velocity = 0
        if physics.crouch_camera_velocity:
            physics.crouch_camera_velocity /= bipd_attrs.camera_collision_and_autoaim.crouch_transition_time

        physics.crouch_camera_velocity /= 30
