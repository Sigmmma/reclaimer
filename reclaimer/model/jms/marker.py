#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsMarker', )

from math import isclose

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
        return (isinstance(other, JmsMarker)
        and self.name == other.name
        and self.permutation == other.permutation
        and self.region == other.region
        and isclose(self.radius, other.radius, rel_tol=0.00001)
        and isclose(self.rot_i,  other.rot_i,  rel_tol=0.00001)
        and isclose(self.rot_j,  other.rot_j,  rel_tol=0.00001)
        and isclose(self.rot_k,  other.rot_k,  rel_tol=0.00001)
        and isclose(self.rot_w,  other.rot_w,  rel_tol=0.00001)
        and isclose(self.pos_x,  other.pos_x,  rel_tol=0.00001)
        and isclose(self.pos_y,  other.pos_y,  rel_tol=0.00001)
        and isclose(self.pos_z,  other.pos_z,  rel_tol=0.00001))
