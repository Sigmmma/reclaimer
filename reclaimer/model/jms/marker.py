#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsMarker', )


class JmsMarker:
    __slots__ = (
        "name", "permutation",
        "region", "parent",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "pos_x", "pos_y", "pos_z",
        "radius",
        )
    def __init__(self, name="", permutation="", region=0, parent=0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0, radius=0.0):
        self.name = name
        self.permutation = permutation
        self.parent = parent
        self.region = max(0, region)
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.radius = radius

    def __repr__(self):
        return """JmsMarker(name=%s,
    permutation=%s,
    region=%s,  parent=%s,
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s,
    radius=%s
)""" % (self.name, self.permutation, self.region, self.parent,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.pos_x, self.pos_y, self.pos_z, self.radius)

    def __eq__(self, other):
        if not isinstance(other, JmsMarker):
            return False
        elif self.name != other.name:
            return False
        elif self.permutation != other.permutation:
            return False
        elif self.region != other.region:
            return False
        elif abs(self.radius - other.radius) > 0.00001:
            return False
        elif (abs(self.rot_i - other.rot_i) > 0.00001 or
              abs(self.rot_j - other.rot_j) > 0.00001 or
              abs(self.rot_k - other.rot_k) > 0.00001 or
              abs(self.rot_w - other.rot_w) > 0.00001):
            return False
        elif (abs(self.pos_x - other.pos_x) > 0.000001 or
              abs(self.pos_y - other.pos_y) > 0.000001 or
              abs(self.pos_z - other.pos_z) > 0.000001):
            return False
        return True
