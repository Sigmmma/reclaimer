#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
import math

from reclaimer.util.matrices import Ray,\
     polar_2d_to_vector_3d, vector_3d_to_polar_2d
from .. import constants as const

class JmaLimpNodeInfo:
    __slots__ = (
        "i", "j", "k", "delta", "axes_free",
        "cross_delta"
        )
    def __init__(self, vector=None, delta=0.0,
                 axes_free=None, joint_flags=None, cross_delta=None
                 ):
        assert axes_free   in (0, 1, 2, None)
        assert isinstance(joint_flags, (int, type(None)))
        assert vector is None or len(vector) in (2, 3)

        i, j, k = (
            (1.0, 0.0, 0.0)         if vector is None or len(vector) != 2 else
            Ray(vector).normalized  if vector        and len(vector) == 3 else
            polar_2d_to_vector_3d(*vector)
            )

        self.i, self.j, self.k, self.delta = i, j, k, delta
        if axes_free is None and joint_flags in (1, 2):
            # math just works out like this
            axes_free = 2-joint_flags

        self.axes_free   = axes_free or 0
        self.cross_delta = (cross_delta or 0) if axes_free == 2 else 0

    # NOTE: the only reason we care about polar coordinates for limp nodes
    #       is because the hinge joints are designed to pivot on y and z,
    #       but not x. in polar coordinates we use x as the reference axis

    @property
    def joint_flags(self):  return 1 << (2 - self.axes_free)
    @property
    def vector_ortho(self): return self.i, self.j, self.k
    @property
    def vector_polar(self): return vector_3d_to_polar_2d(*self.vector_ortho)
    @property
    def vector_range(self): return (self.delta if self.axes_free < 2 else
                                    Ray([self.delta, self.cross_delta]).mag)

    def angle_to_other(self, other):
        i0, j0, k0 = self.i, self.j, self.k
        i1, j1, k1 = (
            other if hasattr(other, "__iter__") else
            (other.i, other.j, other.k)
            )
        mag = ((i0**2 + j0**2 + k0**2) *
               (i1**2 + j1**2 + k1**2)) or 1

        cosine = (i0*i1 + j0*j1 + k0*k1)/mag
        return (0       if cosine >=  1 else
                math.pi if cosine <= -1 else
                math.acos(cosine))

    def __repr__(self):
        return """JmaLimpNodeInfo(
    vector_ortho=%s,
    vector_polar=%s,
    delta=%s, cross_delta=%s, axes_free=%s
)""" % (self.vector_ortho, self.vector_polar, self.delta,
        self.cross_delta, self.axes_free)
