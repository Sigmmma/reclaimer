#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from .. import constants as const

class JmaRootNodeState:
    __slots__ = (
        "dx", "dy", "dz", "dyaw",
        "x", "y", "z", "yaw",
        )
    def __init__(self, dx=0.0, dy=0.0, dz=0.0, dyaw=0.0,
                 x=0.0, y=0.0, z=0.0, yaw=0.0):
        self.dx, self.dy, self.dz, self.dyaw = dx, dy, dz, dyaw
        self.x,  self.y,  self.z,  self.yaw  =  x,  y,  z,  yaw

    def __repr__(self):
        return """JmaRootNodeState(
    dx=%s, dy=%s, dz=%s, dyaw=%s,
    x=%s, y=%s, z=%s, yaw=%s,
)""" % (self.dx, self.dy, self.dz, self.dyaw,
        self.x, self.y, self.z, self.yaw)

    def __eq__(self, other):
        if (not isinstance(other, JmaRootNodeState)           or
            abs(self.dx - other.dx)     > const.TRANS_EPSILON or
            abs(self.dy - other.dy)     > const.TRANS_EPSILON or
            abs(self.dz - other.dz)     > const.TRANS_EPSILON or
            abs(self.dyaw - other.dyaw) > const.DYAW_EPSILON
            ):
            return False
        return True
