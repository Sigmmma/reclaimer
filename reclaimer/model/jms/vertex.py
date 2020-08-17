#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsVertex', )

from math import isclose

class JmsVertex:
    __slots__ = (
        "node_0",
        "pos_x", "pos_y", "pos_z",
        "norm_i", "norm_j", "norm_k",
        "binorm_i", "binorm_j", "binorm_k",
        "tangent_i", "tangent_j", "tangent_k",
        "node_1", "node_1_weight",
        "tex_u", "tex_v", "tex_w",
        "other_nodes", "other_weights", "other_uvws"
        )
    def __init__(self, node_0=0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0,
                 norm_i=0.0, norm_j=0.0, norm_k=1.0,
                 node_1=-1, node_1_weight=0.0,
                 tex_u=0, tex_v=0, tex_w=0,
                 binorm_i=0.0,  binorm_j=1.0,  binorm_k=0.0,
                 tangent_i=1.0, tangent_j=0.0, tangent_k=0.0,
                 other_nodes=(), other_weights=(), other_uvws=()):
        if node_1_weight <= 0:
            node_1 = -1
            node_1_weight = 0

        self.node_0 = node_0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.norm_i = norm_i
        self.norm_j = norm_j
        self.norm_k = norm_k
        self.binorm_i = binorm_i
        self.binorm_j = binorm_j
        self.binorm_k = binorm_k
        self.tangent_i = tangent_i
        self.tangent_j = tangent_j
        self.tangent_k = tangent_k
        self.node_1 = node_1
        self.node_1_weight = node_1_weight
        self.tex_u = tex_u
        self.tex_v = tex_v
        self.tex_w = tex_w
        self.other_nodes = other_nodes
        self.other_weights = other_weights
        self.other_uvws = other_uvws

    def __repr__(self):
        return """JmsVertex(node_0=%s,
    x=%s, y=%s, z=%s,
    i=%s, j=%s, k=%s,
    node_1=%s, node_1_weight=%s,
    u=%s, v=%s, w=%s
)""" % (self.node_0,
        self.pos_x, self.pos_y, self.pos_z,
        self.norm_i, self.norm_j, self.norm_k,
        self.node_1, self.node_1_weight,
        self.tex_u, self.tex_v, self.tex_w)

    def __eq__(self, other):
        return (isinstance(other, JmsVertex)
        and self.name == other.name
        and self.permutation == other.permutation
        and self.region == other.region
        and isclose(self.radius, other.radius, rel_tol=0.00001)

        # Comparing these here might have been a speed optimization?
        and isclose(self.pos_z,  other.pos_z,  rel_tol=0.00001)
        and isclose(self.norm_k, other.norm_k, rel_tol=0.0001)

        and isclose(self.pos_x,  other.pos_x,  rel_tol=0.00001)
        and isclose(self.pos_y,  other.pos_y,  rel_tol=0.00001)

        and isclose(self.norm_i, other.norm_i, rel_tol=0.0001)
        and isclose(self.norm_j, other.norm_j, rel_tol=0.0001)
        # The earlier code did not compare W likely because the effective
        # direction for an inverted W component is the same. But this will cause
        # issues when interpolating normals between vertices (on the triangle).
        and isclose(self.norm_w, other.norm_w, rel_tol=0.0001)

        and isclose(self.node_1_weight, other.node_1_weight, rel_tol=0.0001)

        and self.node_0 == other.node_0
        and self.node_1 == other.node_1

        and isclose(self.tex_u, her.tex_u, rel_tol=0.0001)
        and isclose(self.tex_v, her.tex_v, rel_tol=0.0001))
