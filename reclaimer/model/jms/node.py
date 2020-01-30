#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsNode', )

from ..constants import ( JMS_VERSION_HALO_1, JMS_VERSION_HALO_2_8210, )

class JmsNode:
    __slots__ = (
        "name",
        "first_child", "sibling_index", "parent_index",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "pos_x", "pos_y", "pos_z",
        )
    def __init__(self, name="", first_child=-1, sibling_index=-1,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0, parent_index=-1):
        self.name = name
        self.sibling_index = sibling_index
        self.first_child = first_child
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.parent_index = parent_index

    def __repr__(self):
        return """JmsNode(name=%s,
    first_child=%s, sibling_index=%s,
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s
)""" % (self.name, self.first_child, self.sibling_index,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.pos_x, self.pos_y, self.pos_z)

    def __eq__(self, other):
        if not isinstance(other, JmsNode):
            return False
        elif self.name != other.name:
            return False
        elif self.first_child != other.first_child:
            return False
        elif self.sibling_index != other.sibling_index:
            return False
        elif (abs(self.rot_i - other.rot_i) > 0.00001 or
              abs(self.rot_j - other.rot_j) > 0.00001 or
              abs(self.rot_k - other.rot_k) > 0.00001 or
              abs(self.rot_w - other.rot_w) > 0.00001):
            return False
        elif (abs(self.pos_x - other.pos_x) > 0.00001 or
              abs(self.pos_y - other.pos_y) > 0.00001 or
              abs(self.pos_z - other.pos_z) > 0.00001):
            return False
        return True

    def is_node_hierarchy_equal(self, other):
        if not isinstance(other, JmsNode):
            return False
        elif self.name != other.name:
            return False
        elif self.first_child != other.first_child:
            return False
        elif self.sibling_index != other.sibling_index:
            return False
        return True

    @classmethod
    def setup_node_hierarchy(cls, nodes, jms_version=JMS_VERSION_HALO_1):
        if jms_version == JMS_VERSION_HALO_1:
            # Halo 1
            parented_nodes = set()
            # setup the parent node hierarchy
            for parent_idx in range(len(nodes)):
                node = nodes[parent_idx]
                if node.first_child > 0:
                    sib_idx = node.first_child
                    seen_nodes = set()
                    while sib_idx >= 0:
                        if (sib_idx in seen_nodes or sib_idx == parent_idx or
                            sib_idx >= len(nodes)):
                            break
                        seen_nodes.add(sib_idx)
                        parented_nodes.add(sib_idx)
                        sib_node = nodes[sib_idx]
                        sib_node.parent_index = parent_idx
                        sib_idx = sib_node.sibling_index
        elif jms_version == JMS_VERSION_HALO_2_8210:
            # Halo 2
            pass
