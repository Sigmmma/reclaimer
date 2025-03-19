#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from reclaimer.util.matrices import Quaternion
from .. import constants as const

class JmaNodeState:
    __slots__ = (
        "pos_x", "pos_y", "pos_z",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "scale",
        )
    def __init__(self, pos_x=0.0, pos_y=0.0, pos_z=0.0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0, scale=1.0):
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.scale = scale

    @property
    def quat(self):
        return Quaternion((self.rot_i, self.rot_j, self.rot_k, self.rot_w))

    def __repr__(self):
        return """JmaNodeState(
    x=%s, y=%s, z=%s,
    i=%s, j=%s, k=%s, w=%s,
    scale=%s
)""" % (self.pos_x, self.pos_y, self.pos_z,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.scale)

    def __eq__(self, other):
        if (not isinstance(other, JmaNodeState)                 or
            abs(self.rot_i - other.rot_i) > const.QUAT_EPSILON  or
            abs(self.rot_j - other.rot_j) > const.QUAT_EPSILON  or
            abs(self.rot_k - other.rot_k) > const.QUAT_EPSILON  or
            abs(self.rot_w - other.rot_w) > const.QUAT_EPSILON  or
            abs(self.pos_x - other.pos_x) > const.TRANS_EPSILON or
            abs(self.pos_y - other.pos_y) > const.TRANS_EPSILON or
            abs(self.pos_z - other.pos_z) > const.TRANS_EPSILON or
            abs(self.scale - other.scale) > const.SCALE_EPSILON
            ):
            return False
        return True

    def __sub__(self, other):
        if not isinstance(other, JmaNodeState):
            raise TypeError("Cannot subtract %s from %s" %
                            (type(other), type(self)))
        return JmaNodeState(
            self.pos_x - other.pos_x, self.pos_y - other.pos_y,
            self.pos_z - other.pos_z, self.rot_i - other.rot_i,
            self.rot_j - other.rot_j, self.rot_k - other.rot_k,
            self.rot_w - other.rot_w, self.scale - other.scale,
            )
